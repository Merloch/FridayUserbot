# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters

from database.filterdb import (
    add_filters,
    all_filters,
    del_filters,
    filters_del,
    filters_info,
)
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["delfilter"],
    cmd_help={"help": "Delete A Filter!", "example": "{ch}delfilter (filter name)"},
)
async def del_filterz(client, message):
    note_ = await edit_or_reply(message, "`Processing..`")
    note_name = get_text(message)
    if not note_name:
        await note_.edit("`Give A Filter Name!`")
        return
    note_name = note_name.lower()
    if not await filters_info(note_name, int(message.chat.id)):
        await note_.edit("`Filter Not Found!`")
        return
    await del_filters(note_name, int(message.chat.id))
    await note_.edit(f"`Filter {note_name} Deleted Successfully!`")


@friday_on_cmd(
    ["filters"],
    cmd_help={"help": "List All The Filters In The Chat!", "example": "{ch}filters"},
)
async def show_filters(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    poppy = await all_filters(int(message.chat.id))
    if poppy is False:
        await pablo.edit("`No Filters Found In This Chat...`")
        return
    kk = ""
    for Escobar in poppy:
        kk += f"\n > `{Escobar.get('keyword')}`"
    X = await client.get_chat(int(message.chat.id))
    grp_nme = X.title
    mag = f"List Of Filters In {grp_nme}: \n{kk}"
    await pablo.edit(mag)


@friday_on_cmd(
    ["savefilter"],
    cmd_help={
        "help": "Save A Filter!",
        "example": "{ch}savefilter (filter name) (replying to message)",
    },
)
async def s_filters(client, message):
    note_ = await edit_or_reply(message, "`Processing..`")
    note_name = get_text(message)
    if not note_name:
        await note_.edit("`Give A Filter Name!`")
        return
    if not message.reply_to_message:
        await note_.edit("Reply To Message To Save As Filter!")
        return
    note_name = note_name.lower()
    msg = message.reply_to_message
    copied_msg = await msg.copy(int(Config.LOG_GRP))
    await add_filters(note_name, int(message.chat.id), copied_msg.message_id)
    await note_.edit(f"`Done! {note_name} Added To Filters List!`")


@listen(filters.incoming & ~filters.edited & filters.group)
async def filter_s(client, message):
    owo = message.text
    al_fill = []
    if not owo:
        message.continue_propagation()
        return
    al_fil = await all_filters(int(message.chat.id))
    if not al_fil:
        message.continue_propagation()
        return
    for all_fil in al_fil:
        al_fill.append(all_fil.get('keyword'))
    owoo = owo.lower()
    if owoo in al_fill:
        f_info = await filters_info(owoo, int(message.chat.id))
        if f_info:
            await client.copy_message(
                    from_chat_id=int(Config.LOG_GRP),
                    chat_id=int(message.chat.id),
                    message_id=f_info["msg_id"],
                    reply_to_message_id=message.message_id,
             )
    message.continue_propagation()


@friday_on_cmd(
    ["delfilters"],
    cmd_help={"help": "Delete All The Filters in chat!", "example": "{ch}delfilters"},
)
async def del_all_filters(client, message):
    pablo = await edit_or_reply(message, "`Processing...`")
    poppy = await all_filters(int(message.chat.id))
    if poppy is False:
        await pablo.edit("`No Filters Found In This Chat...`")
        return
    await filters_del(int(message.chat.id))
    await pablo.edit("Deleted All The Filters Successfully!!")
