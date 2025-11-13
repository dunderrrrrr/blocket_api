from unittest.mock import MagicMock, patch

import respx
from httpx import Response

from blocket_api.blocket import BlocketAPI
from blocket_api.constants import BASE_URL, SENDBIRD_URL

api = BlocketAPI("token")


class Test_Sendbird:
    @respx.mock
    @patch("blocket_api.sendbird.SendbirdClient.get_data")
    def test_get_threats(self, mock_get_data: MagicMock) -> None:
        respx.get(f"{BASE_URL}/messaging-sendbird-communication/v1/users/tokens").mock(
            return_value=Response(
                status_code=200,
                json={
                    "expires_at": 1763061949,
                    "sb_session_token": "token",
                    "sb_user_id": "c1-user-id",
                    "verification_token": "token.data",
                },
            ),
        )

        # Mock the SendbirdClient.get_data() response
        # this is pretty much what the wss returns
        mock_get_data.return_value = '{"user_id":"c1-user-id","nickname":"Username","profile_url":"","require_auth_for_profile_image":false,"ekey":"key","metadata":{"is_migrated":"true"},"is_hide_me_from_friends":false,"ping_interval":15,"pong_timeout":5,"login_ts":1763058491682,"reconnect":{"max_interval":20,"interval":2,"retry_cnt":-1,"mul":2},"bc_duration":0,"preferred_languages":[],"max_unread_cnt_on_super_group":100,"unread_cnt_threading_policy":0,"last_msg_threading_policy":0,"use_reaction":true,"disable_supergroup_mack":false,"multiple_file_send_max_size":30,"request_dedup_interval_ms":500,"allow_log_publish":true,"log_publish_config":{"default":{"min_stat_count":100,"min_interval":10800,"max_stat_count_per_request":1000,"lower_threshold":10,"request_delay_range":180},"realtime":{"min_stat_count":1,"min_interval":0,"max_stat_count_per_request":1000,"lower_threshold":0,"request_delay_range":20}},"key":"session-key","expires_at":-1,"unread_cnt":{"all":0,"ts":1763058491692},"discovery_keys":[],"file_upload_size_limit":50,"premium_feature_list":["ai_chatbot","chat_uikit_sdk_access","knowledge_uptodate","remove_powered_by","ai_chatbot_data_export","knowledge_ingestion_additional_source","ai_engine","data_export","moderation_open","moderation_group","auto_thumbnail","bot_interface","migration","profanity_filter","domain_filter","image_moderation","analytics","analytics_v2","reactions","salesforce_extension_ai"],"emoji_hash":"","notifications":{"enabled":false,"feed_channels":{},"template_list_token":"0","settings_updated_at":0},"application_attributes":["enable_message_threading","reactions","use_last_seen_at","allow_group_channel_leave_from_sdk","allow_group_channel_delete_from_sdk","allow_non_operators_to_mention_channel","allow_only_operator_sdk_to_update_group_channel_name","allow_only_operator_sdk_to_update_group_channel_image","allow_operators_to_edit_operators","allow_operators_to_ban_operators","allow_message_update_from_sdk","allow_anonymous_message_update","allow_message_delete_from_sdk","allow_operator_message_delete","allow_migration_api","allow_file_messages_from_sdk","allow_sdk_file_message_urls","allow_non_owner_message_fetch_from_sdk","allow_emoji_create_from_sdk","allow_emoji_update_from_sdk","allow_emoji_delete_from_sdk","allow_emoji_category_create_from_sdk","allow_emoji_category_update_from_sdk","allow_emoji_category_delete_from_sdk","allow_emoji_update_from_different_user","allow_emoji_delete_from_different_user","allow_emoji_category_update_from_different_user","allow_emoji_category_delete_from_different_user","allow_sdk_noti_stats_log_publish","allow_sdk_feature_local_cache_log_publish","remove_powered_by"],"config_sync_needed":false,"services":["chat"]}'

        respx.get(
            f"{SENDBIRD_URL}/v3/users/c1-user-id/my_group_channels?token=&limit=15&order=latest_last_message&show_member=true&show_read_receipt=true&show_delivery_receipt=true&show_empty=false&member_state_filter=all&super_mode=all&public_mode=all&unread_filter=all&name_contains=&custom_type_startswith=&hidden_mode=unhidden_only&show_frozen=true&show_metadata=true&include_chat_notification=false&include_left_channel=false"
        ).mock(
            return_value=Response(
                status_code=200,
                json={
                    "channels": [
                        {
                            "channel_url": "sendbird_group_channel_123",
                            "name": "from:id,ad:1214281684,to:c1-user-id",
                            "cover_url": "https://static.sendbird.com/sample/cover/cover_12.jpg",
                            "data": "data",
                        },
                        {
                            "channel_url": "sendbird_group_channel_123",
                            "name": "from:id,ad:1214281684,to:c1-user-id",
                            "cover_url": "https://static.sendbird.com/sample/cover/cover_12.jpg",
                            "data": "data",
                        },
                    ],
                },
            ),
        )
        assert api.get_threads() == {
            "channels": [
                {
                    "channel_url": "sendbird_group_channel_123",
                    "name": "from:id,ad:1214281684,to:c1-user-id",
                    "cover_url": "https://static.sendbird.com/sample/cover/cover_12.jpg",
                    "data": "data",
                },
                {
                    "channel_url": "sendbird_group_channel_123",
                    "name": "from:id,ad:1214281684,to:c1-user-id",
                    "cover_url": "https://static.sendbird.com/sample/cover/cover_12.jpg",
                    "data": "data",
                },
            ]
        }

    @respx.mock
    @patch("blocket_api.sendbird.SendbirdClient.get_data")
    def test_get_messages_from_thread(self, mock_get_data: MagicMock) -> None:
        respx.get(f"{BASE_URL}/messaging-sendbird-communication/v1/users/tokens").mock(
            return_value=Response(
                status_code=200,
                json={
                    "expires_at": 1763061949,
                    "sb_session_token": "token",
                    "sb_user_id": "c1-user-id",
                    "verification_token": "token.data",
                },
            ),
        )

        # Mock the SendbirdClient.get_data() response
        # this is pretty much what the wss returns
        mock_get_data.return_value = '{"user_id":"c1-user-id","nickname":"Username","profile_url":"","require_auth_for_profile_image":false,"ekey":"key","metadata":{"is_migrated":"true"},"is_hide_me_from_friends":false,"ping_interval":15,"pong_timeout":5,"login_ts":1763058491682,"reconnect":{"max_interval":20,"interval":2,"retry_cnt":-1,"mul":2},"bc_duration":0,"preferred_languages":[],"max_unread_cnt_on_super_group":100,"unread_cnt_threading_policy":0,"last_msg_threading_policy":0,"use_reaction":true,"disable_supergroup_mack":false,"multiple_file_send_max_size":30,"request_dedup_interval_ms":500,"allow_log_publish":true,"log_publish_config":{"default":{"min_stat_count":100,"min_interval":10800,"max_stat_count_per_request":1000,"lower_threshold":10,"request_delay_range":180},"realtime":{"min_stat_count":1,"min_interval":0,"max_stat_count_per_request":1000,"lower_threshold":0,"request_delay_range":20}},"key":"session-key","expires_at":-1,"unread_cnt":{"all":0,"ts":1763058491692},"discovery_keys":[],"file_upload_size_limit":50,"premium_feature_list":["ai_chatbot","chat_uikit_sdk_access","knowledge_uptodate","remove_powered_by","ai_chatbot_data_export","knowledge_ingestion_additional_source","ai_engine","data_export","moderation_open","moderation_group","auto_thumbnail","bot_interface","migration","profanity_filter","domain_filter","image_moderation","analytics","analytics_v2","reactions","salesforce_extension_ai"],"emoji_hash":"","notifications":{"enabled":false,"feed_channels":{},"template_list_token":"0","settings_updated_at":0},"application_attributes":["enable_message_threading","reactions","use_last_seen_at","allow_group_channel_leave_from_sdk","allow_group_channel_delete_from_sdk","allow_non_operators_to_mention_channel","allow_only_operator_sdk_to_update_group_channel_name","allow_only_operator_sdk_to_update_group_channel_image","allow_operators_to_edit_operators","allow_operators_to_ban_operators","allow_message_update_from_sdk","allow_anonymous_message_update","allow_message_delete_from_sdk","allow_operator_message_delete","allow_migration_api","allow_file_messages_from_sdk","allow_sdk_file_message_urls","allow_non_owner_message_fetch_from_sdk","allow_emoji_create_from_sdk","allow_emoji_update_from_sdk","allow_emoji_delete_from_sdk","allow_emoji_category_create_from_sdk","allow_emoji_category_update_from_sdk","allow_emoji_category_delete_from_sdk","allow_emoji_update_from_different_user","allow_emoji_delete_from_different_user","allow_emoji_category_update_from_different_user","allow_emoji_category_delete_from_different_user","allow_sdk_noti_stats_log_publish","allow_sdk_feature_local_cache_log_publish","remove_powered_by"],"config_sync_needed":false,"services":["chat"]}'

        respx.get(
            f"{SENDBIRD_URL}/v3/group_channels/channel_id/messages?is_sdk=true&prev_limit=30&next_limit=0&include=false&reverse=false&message_ts=9007199254740991&message_type=&include_reply_type=none&with_sorted_meta_array=false&include_reactions=false&include_thread_info=false&include_parent_message_info=false&show_subchannel_message_only=false&include_poll_details=true"
        ).mock(
            return_value=Response(
                status_code=200,
                json={
                    "messages": [
                        {
                            "type": "MESG",
                            "message_id": 1354993570,
                            "message": "Hey whats up ",
                        },
                        {
                            "type": "MESG",
                            "message_id": 1354993570,
                            "message": "All good m8",
                        },
                    ]
                },
            ),
        )
        assert api.get_messages_from_thread("channel_id") == {
            "messages": [
                {"type": "MESG", "message_id": 1354993570, "message": "Hey whats up "},
                {"type": "MESG", "message_id": 1354993570, "message": "All good m8"},
            ]
        }
