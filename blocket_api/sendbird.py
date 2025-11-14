from __future__ import annotations

import json
import time
import urllib.parse
from dataclasses import dataclass

import httpx
from pydantic import BaseModel, ConfigDict
from websockets.sync.client import connect

from .constants import BASE_URL, BLOCKET_SENDBIRD_APP_ID, SENDBIRD_URL

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0"


class SendbirdResponse(BaseModel):
    user_id: str
    nickname: str
    profile_url: str
    ekey: str
    metadata: dict

    ping_interval: int
    pong_timeout: int
    login_ts: int

    key: str  # Session key
    expires_at: int

    unread_cnt: dict
    premium_feature_list: list[str]
    application_attributes: list[str]
    services: list[str]

    model_config = ConfigDict(extra="ignore")

    @property
    def session_key(self) -> str:
        return self.key


def get_blocket_tokens(bearer_token: str) -> dict:
    token_response = httpx.get(
        f"{BASE_URL}/messaging-sendbird-communication/v1/users/tokens",
        headers={
            "Authorization": f"Bearer {bearer_token}",
        },
    )
    token_response.raise_for_status()
    return token_response.json()


class SendbirdClient:
    def __init__(
        self,
        app_id: str,
        user_id: str,
        access_token: str,
    ):
        self.app_id = app_id
        self.user_id = user_id
        self.access_token = access_token

    def _build_wss_url(self) -> str:
        base_url = f"wss://ws-{self.app_id.lower()}.sendbird.com/"
        timestamp = str(int(time.time() * 1000))

        params = {
            "p": "JS",
            "pv": USER_AGENT,
            "sv": "4.10.8",
            "ai": self.app_id,
            "pmce": "1",
            "active": "1",
            "device_token_types": "gcm,huawei,apns",
            "SB-User-Agent": "JS/c4.10.8///oweb",
            "SB-SDK-User-Agent": "main_sdk_info=chat/js/4.10.8&device_os_platform=web&os_version=Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Request-Sent-Timestamp": timestamp,
            "include_extra_data": "premium_feature_list,file_upload_size_limit,application_attributes,emoji_hash,multiple_file_send_max_size,notifications",
            "use_local_cache": "0",
            "include_poll_details": "1",
            "user_id": self.user_id,
        }

        return base_url + "?" + urllib.parse.urlencode(params)

    def get_data(self) -> str:
        with connect(
            self._build_wss_url(),
            subprotocols=[urllib.parse.quote(json.dumps({"token": self.access_token}))],  # type: ignore[list-item]
            additional_headers={
                "User-Agent": USER_AGENT,
                "Origin": "https://www.blocket.se",
            },
            open_timeout=5,
        ) as websocket:
            message: str = websocket.recv(timeout=5)  # type: ignore[assignment]
            return str(message.split("LOGI")[1])


@dataclass(frozen=True)
class Sendbird:
    sendbird_client: SendbirdClient

    @classmethod
    def generate(cls, blocket_token: str) -> Sendbird:
        tokens = get_blocket_tokens(blocket_token)
        sb_token = tokens["sb_session_token"]
        sb_user_id = tokens["sb_user_id"]
        return cls(
            sendbird_client=SendbirdClient(
                app_id=BLOCKET_SENDBIRD_APP_ID,
                user_id=sb_user_id,
                access_token=sb_token,
            )
        )

    def get_threads(self, limit: int) -> dict:
        sendbird = SendbirdResponse.model_validate_json(self.sendbird_client.get_data())
        response = httpx.get(
            f"{SENDBIRD_URL}/v3/users/{self.sendbird_client.user_id}/my_group_channels",
            params={
                "token": "",
                "limit": limit,
                "order": "latest_last_message",
                "show_member": True,
                "show_read_receipt": True,
                "show_delivery_receipt": True,
                "show_empty": False,
                "member_state_filter": "all",
                "super_mode": "all",
                "public_mode": "all",
                "unread_filter": "all",
                "name_contains": "",
                "custom_type_startswith": "",
                "hidden_mode": "unhidden_only",
                "show_frozen": True,
                "show_metadata": True,
                "include_chat_notification": False,
                "include_left_channel": False,
            },
            headers={
                "Session-Key": sendbird.session_key,
                "Access-Token": self.sendbird_client.access_token,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_messages_from_thread(self, channel_id: str) -> dict:
        sendbird = SendbirdResponse.model_validate_json(self.sendbird_client.get_data())
        response = httpx.get(
            f"{SENDBIRD_URL}/v3/group_channels/{channel_id}/messages",
            params={
                "is_sdk": True,
                "prev_limit": 30,
                "next_limit": 0,
                "include": False,
                "reverse": False,
                "message_ts": 9007199254740991,
                "message_type": "",
                "include_reply_type": "none",
                "with_sorted_meta_array": False,
                "include_reactions": False,
                "include_thread_info": False,
                "include_parent_message_info": False,
                "show_subchannel_message_only": False,
                "include_poll_details": True,
            },
            headers={
                "Session-Key": sendbird.session_key,
                "Access-Token": self.sendbird_client.access_token,
            },
        )
        response.raise_for_status()
        return response.json()

    def unread_messages_count(self) -> dict:
        sendbird = SendbirdResponse.model_validate_json(self.sendbird_client.get_data())
        response = httpx.get(
            f"{SENDBIRD_URL}/v3/users/{self.sendbird_client.user_id}/unread_message_count",
            params={"super_mode": "all", "include_feed_channel": False},
            headers={
                "Session-Key": sendbird.session_key,
                "Access-Token": self.sendbird_client.access_token,
            },
        )
        response.raise_for_status()
        return response.json()
