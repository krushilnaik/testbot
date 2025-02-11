from time import sleep

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ActionTypes, CardAction, ChannelAccount, SuggestedActions


class MyBot(ActivityHandler):
    async def on_members_added_activity(self, members_added: list[ChannelAccount], turn_context: TurnContext):
        """
        Send a welcome message to the user and tell them what actions they may perform to use this bot
        """

        return await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to the users choice and display the suggested actions again.
        """

        text = turn_context.activity.text.lower()
        response_text = self._process_input(text)

        if isinstance(response_text, str):
            await turn_context.send_activity(MessageFactory.text(response_text))
        else:
            await turn_context.send_activity(response_text)

    def _get_welcome_message(self):
        reply = MessageFactory.text(f"Welcome to CAF Bot. Click a thing or ask a thing.\n\n[test](www.google.com)")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="CAF Governance",
                    type=ActionTypes.im_back,
                    value="CAF Governance",
                ),
                CardAction(
                    title="Investment Requests",
                    type=ActionTypes.im_back,
                    value="Investment Requests",
                ),
                CardAction(
                    title="Third one",
                    type=ActionTypes.im_back,
                    value="Third one",
                ),
            ]
        )

        return reply

    async def _send_welcome_message(self, turn_context: TurnContext):
        if turn_context.activity.members_added:
            for member in turn_context.activity.members_added:
                if turn_context.activity.recipient and member.id != turn_context.activity.recipient.id:
                    reply = self._get_welcome_message()
                    await turn_context.send_activity(reply)

                    # await self._send_suggested_actions(turn_context)

    def _ask_ai(self, text: str):
        sleep(5)

        return f"ai generated response for: '{text}'"

    def _start_investment_request(self):
        pass

    def _process_input(self, text: str):
        print(f"user response: '{text}'")

        match text:
            case "restart":
                return self._get_welcome_message()
            case "caf governance":
                reply = MessageFactory.text("You clicked on CAF Governance")

                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title="More specific question 1", type=ActionTypes.im_back, value="More specific question 1"
                        ),
                        CardAction(
                            title="More specific question 2", type=ActionTypes.im_back, value="More specific question 2"
                        ),
                    ]
                )
            case "investment requests":
                reply = MessageFactory.text("You clicked on CAF Governance")

                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title="More specific question 1", type=ActionTypes.im_back, value="More specific question 1"
                        ),
                        CardAction(
                            title="More specific question 2", type=ActionTypes.im_back, value="More specific question 2"
                        ),
                    ]
                )
            case _:
                return self._ask_ai(text)

        return reply
