from telethon import TelegramClient, events, Button
import json
import os
import asyncio


# ==========================================
# 🤖 BOT CONFIG
# ==========================================

API_ID = 39185757
API_HASH = "10582578860a17487c7454b111df66f6"
BOT_TOKEN = "8865964956:AAHMbZygLAD6M29S3QohAZ-BfDNeA59yUdg"

# আপনার Telegram User ID
OWNER_ID = 8514407577

GROUP_FILE = "groups.json"

client = TelegramClient(
    "admin_panel_bot",
    API_ID,
    API_HASH
)


# ==========================================
# 💾 GROUP DATABASE
# ==========================================

def load_groups():

    if not os.path.exists(GROUP_FILE):
        return []

    try:

        with open(
            GROUP_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except Exception as e:

        print(
            f"❌ Group Load Error: {e}"
        )

    return []


# ==========================================
# 🔐 ADMIN CHECK
# ==========================================

def is_admin(user_id):

    return int(user_id) == int(OWNER_ID)


# ==========================================
# 🏠 ADMIN PANEL
# ==========================================

def admin_panel_buttons():

    return [
        [
            Button.inline(
                "📢 Broadcast Message",
                b"broadcast"
            )
        ],
        [
            Button.inline(
                "👥 Group List",
                b"group_list"
            ),
            Button.inline(
                "📊 Statistics",
                b"statistics"
            )
        ],
        [
            Button.inline(
                "🔄 Refresh",
                b"admin_panel"
            )
        ]
    ]


# ==========================================
# /ADMIN
# ==========================================

@client.on(
    events.NewMessage(
        pattern=r"^/admin$"
    )
)
async def admin_command(event):

    if not is_admin(
        event.sender_id
    ):

        await event.reply(
            "❌ You are not authorized."
        )

        return

    groups = load_groups()

    await event.reply(
        "👑 **Aᴅᴍɪɴ Pᴀɴᴇʟ**\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 **Tᴏᴛᴀʟ Gʀᴏᴜᴘꜱ:** `{len(groups)}`\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select an option below:",
        buttons=admin_panel_buttons()
    )


# ==========================================
# 🔘 ADMIN PANEL CALLBACK
# ==========================================

@client.on(
    events.CallbackQuery()
)
async def admin_callbacks(event):

    if not is_admin(
        event.sender_id
    ):

        await event.answer(
            "❌ Unauthorized",
            alert=True
        )

        return


    data = event.data.decode(
        "utf-8"
    )


    # ======================================
    # 🏠 ADMIN PANEL
    # ======================================

    if data == "admin_panel":

        groups = load_groups()

        await event.edit(
            "👑 **Aᴅᴍɪɴ Pᴀɴᴇʟ**\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **Tᴏᴛᴀʟ Gʀᴏᴜᴘꜱ:** `{len(groups)}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Select an option below:",
            buttons=admin_panel_buttons()
        )

        return


    # ======================================
    # 📊 STATISTICS
    # ======================================

    if data == "statistics":

        groups = load_groups()

        await event.edit(
            "📊 **Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs**\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **Tᴏᴛᴀʟ Gʀᴏᴜᴘꜱ:** `{len(groups)}`\n"
            "🤖 **Bᴏᴛ Sᴛᴀᴛᴜs:** `ONLINE`\n"
            "━━━━━━━━━━━━━━━━━━━━",
            buttons=[
                [
                    Button.inline(
                        "🔙 Back",
                        b"admin_panel"
                    )
                ]
            ]
        )

        return


    # ======================================
    # 👥 GROUP LIST
    # ======================================

    if data == "group_list":

        groups = load_groups()

        if not groups:

            text = (
                "👥 **Gʀᴏᴜᴘ Lɪsᴛ**\n\n"
                "No groups found."
            )

        else:

            lines = []

            for index, group_id in enumerate(
                groups,
                start=1
            ):

                lines.append(
                    f"`{index}.` `{group_id}`"
                )

            text = (
                "👥 **Gʀᴏᴜᴘ Lɪsᴛ**\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                + "\n".join(lines)
                + "\n━━━━━━━━━━━━━━━━━━━━"
            )

        await event.edit(
            text,
            buttons=[
                [
                    Button.inline(
                        "🔙 Back",
                        b"admin_panel"
                    )
                ]
            ]
        )

        return


    # ======================================
    # 📢 BROADCAST
    # ======================================

    if data == "broadcast":

        client._broadcast_users = getattr(
            client,
            "_broadcast_users",
            set()
        )

        client._broadcast_users.add(
            event.sender_id
        )

        await event.edit(
            "📢 **Bʀᴏᴀᴅᴄᴀsᴛ Mᴏᴅᴇ**\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Send the message you want to broadcast.\n\n"
            "The message will be sent to all "
            "saved groups.\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "❌ Send `/cancel` to cancel."
        )

        return


# ==========================================
# 📢 BROADCAST MESSAGE HANDLER
# ==========================================

@client.on(
    events.NewMessage()
)
async def broadcast_handler(event):

    if event.sender_id is None:
        return

    if not is_admin(
        event.sender_id
    ):
        return

    broadcast_users = getattr(
        client,
        "_broadcast_users",
        set()
    )

    if event.sender_id not in broadcast_users:
        return

    # Ignore admin command
    if event.raw_text.strip() == "/admin":
        return


    # ======================================
    # ❌ CANCEL
    # ======================================

    if event.raw_text.strip() == "/cancel":

        broadcast_users.discard(
            event.sender_id
        )

        await event.reply(
            "❌ **Broadcast cancelled.**"
        )

        return


    groups = load_groups()

    if not groups:

        broadcast_users.discard(
            event.sender_id
        )

        await event.reply(
            "❌ No groups found."
        )

        return


    # ======================================
    # 🚀 START BROADCAST
    # ======================================

    broadcast_users.discard(
        event.sender_id
    )

    status_message = await event.reply(
        "📢 **Broadcast Started...**\n\n"
        f"👥 Groups: `{len(groups)}`\n"
        "⏳ Please wait..."
    )


    success = 0
    failed = 0


    for group_id in groups:

        try:

            # Send the exact message/content
            await client.send_message(
                group_id,
                event.message
            )

            success += 1

            await asyncio.sleep(
                1
            )

        except Exception as e:

            failed += 1

            print(
                f"❌ Broadcast Error "
                f"{group_id}: {e}"
            )


    # ======================================
    # 📊 BROADCAST RESULT
    # ======================================

    await status_message.edit(
        "✅ **Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇ**\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📤 **Sent:** `{success}`\n"
        f"❌ **Failed:** `{failed}`\n"
        f"👥 **Total:** `{len(groups)}`\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )


# ==========================================
# 🚀 START BOT
# ==========================================

print(
    "🤖 Admin Panel Bot Started..."
)

client.start(
    bot_token=BOT_TOKEN
)

client.run_until_disconnected()
