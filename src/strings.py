"""String file"""

from datetime import datetime

from aiogram.utils.markdown import hbold


class Strings:
    """Strings class."""

    def __init__(self) -> None:
        """Initialize the strings class."""
        pass

    def echo_message(self, message: str) -> str:
        """Echo message."""
        return f"You said {message}"

    def done_message(self) -> str:
        """Done message."""
        return "Done!"

    def can_create_subscription_message(self) -> str:
        """Can create subscription message."""
        return "You can now subscribe to a subscription plan. Use /subscription to see available plans."

    def welcome_message(self, username: str) -> str:
        """Welcome message with subscription info."""
        text = (
            f"Hello {hbold(username)},\n"
            "Welcome to QuiverTech's Past Questions Bot!\n\n"
            "Here's how you can get started:\n"
            "- Type the name of the past question you're looking for (e.g., ugbs 104, dcit 103, math 122, ugrc 110).\n"
            "- Select the one you want, and it'll be sent to you directly at a fee of 1 cedi.\n\n"
            "Looking for more? Explore our Subscription Tiers /subscription:\n"
            "For more details, check the /help section."
        )
        return text

    def unauthorized_user_message(self) -> str:
        """Unauthorized user message."""
        return "You haven't registered yet. Please type the /start command to register."

    def invalid_past_question_message(self) -> str:
        """Invalid past question message."""
        text = (
            f"{hbold('Invalid past question name')}\n\n"
            "Please enter a valid past question name.\n"
            "Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 )"
        )
        return text

    def searching_past_question_message(self, past_question_name: str) -> str:
        """Searching past question message."""
        return f"""Searching for {past_question_name} past questions..."""

    def no_past_question_found_message(self, past_question_name: str) -> str:
        """No past question found message."""
        return f"No {past_question_name} past question found."

    def found_past_question_message(self, length: int, past_question_name: str) -> str:
        """Found past question message."""
        return f"""We found {length} {past_question_name} past questions."""

    def past_questions_title_message(self, past_question_name: str) -> str:
        """Past questions title message."""
        return f"{past_question_name} Past Questions\n\n"

    def past_question_to_download_message(self) -> str:
        """Past question to download message."""
        return "Which one do you want to download."

    def sending_all_past_questions_message(self) -> str:
        """Sending all past questions message."""
        return "Sending all past questions..."

    def sending_past_question_message(self) -> str:
        """Sending past question message."""
        return "Sending past question..."

    def failed_to_get_past_question_message(self, past_question_name: str = "") -> str:
        """Failed to get past question message."""
        if not past_question_name:
            return "Failed to get past question."
        return f"Failed to get {past_question_name} past question."

    def invalid_type_message(self) -> str:
        """Invalid type message."""
        return (
            "Invalid type. Please type the past questions course name and course code."
        )

    def help_message(self) -> str:
        """Help message."""
        text = (
            f"{hbold('Help')}\n\n"
            f"{hbold('Commands')}\n"
            "The following commands are available:\n\n"
            "/start -> Register.\n"
            "/subscription -> View subscription plans.\n"
            "/subscribe -> Subscribe to a plan.\n"
            "/view -> View your subscriptions\n"
            "/help -> This Message.\n\n"
            f"{hbold('How to use this bot.')}\n"
            "To request a past question please type the past questions course name and course code.\n"
            "Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 ).\n"
            "A past question costs 1 cedi and there are tiers you can subscribe to via the /subscription command\n"
            "You can also opt for a Pay As You Go model, where you pay 1 Cedi per past question.\n\n"
            "Thank you for using QuiverTech's Past Questions Bot. Have a nice day!"
        )
        return text

    def no_active_subscription_message(self) -> str:
        """No active subscription message."""
        return "You don't have an active subscription. Please subscribe to a plan via /subscription."

    def update_past_question_number(self, downloaded: int, balance: int) -> str:
        """Update past question number."""
        new_balance = balance - downloaded
        return f"""You downloaded {downloaded} past question{'' if new_balance else's'}. You current balance is {new_balance} past questions left.\n You can top up with /subscribe. Tap on /subscription to view the subscription plans."""

    def already_registered_message(self, past_question_name: str) -> str:
        """Already registered message."""
        text = (
            f"Hello, {past_question_name},\nYou are already  registered!\n\n"
            "To request a past question please type the past questions course name and course code.\n"
            "Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 ).\n"
            "For more information, use /help."
        )
        return text

    def current_subscription_message(self, subscription_plan: str, balance: int) -> str:
        """Current subscription message."""
        text = (
            f"{hbold('Current Subscription')}\n"
            f"Subscription Plan: {subscription_plan}\n"
            f"Balance: {balance} past questions left."
        )
        return text

    def make_payment_message(self, url: str, subscription_plan: str = "") -> str:
        """Make payment message."""
        if not subscription_plan:
            return f"Click on the link below to make payment.\n\n({url})"
        return f"Click on the link below to make payment for the {subscription_plan} subscription plan.\n\n({url})"

    def completed_payment_question_message(self) -> str:
        """Completed payment question message."""
        return "Have you completed your payment?"

    def creating_payment_link(self) -> str:
        """Creating payment link message."""
        return "Creating payment link..."

    def create_payment_failed_message(self) -> str:
        """Failed payment message."""
        return "Failed to create payment link. Please try again later."

    def daquiver_easter_egg_message(self) -> str:
        """Daquiver easter egg message."""
        return "Daquiver is the best!"

    def failed_to_subscribe(self) -> str:
        """Failed to subscribe message."""
        return "Failed to subscribe. Please contact @daquiver immediately!"

    def subscription_successful_message(
        self, subscription_plan: str, balance: int
    ) -> str:
        """Subscription successful message."""
        text = (
            f"You have successfully subscribed to the {subscription_plan} subscription plan.\n"
            f"You currently have a balance of {balance} past questions left.\n\n"
            "Go ahead and download a past question. Eg: DCIT 104"
        )
        return text

    def payment_not_started_message(self) -> str:
        """Payment not started message."""
        return "Payment not started. Please start payment process."

    def payment_failed_message(self) -> str:
        """Payment failed message."""
        return "Payment failed. Please try again."

    def payment_successful_message(self) -> str:
        """Payment successful message."""
        return "Payment successful..."

    def payment_verification_failed_message(self) -> str:
        """Payment verification failed message."""
        return "Payment verification failed. Please try again."

    def subscription_info_message(self) -> str:
        """Subscription information message."""
        subscription_details = (
            f"{hbold('Subscription Tiers:')}\n"
            "- Basic: 5 Cedis for 7 past questions\n"
            "- Standard: 10 Cedis for 15 past questions\n"
            "- Premium: 15 Cedis for 25 past questions\n\n"
            f"{hbold('Pay As You Go Model:')}\n"
            "Don't want to subscribe? No problem! You can also opt for a Pay As You Go model, where you pay 1 Cedi per past question.\n\n"
            "Use /subscribe (tier) to subscribe to a tier [eg: /subscribe standard]\n"
            "Or simply ask for a past question to use the Pay As You Go model."
        )
        return subscription_details

    def specify_subscription_tier_message(self) -> str:
        """Specify subscription tier."""
        return "Please specify a subscription tier. Use /subscription to see available tiers."

    def invalid_subscription_tier_message(self, text: str) -> str:
        """Invalid subscription tier."""
        return f"You typed {text}. Invalid subscription tier. Use /subscription to see available tiers."

    def subscribing_to_tier_message(self, tier: str) -> str:
        """Subscribing to tier message."""
        return f"Subscribing to {tier} plan..."

    def no_active_subscription_message(self) -> str:
        """No active subscription message."""
        return "You don't have an active subscription. So initiating pay as you go model. Use /subscription to see available plans."

    def selected_all_message(self) -> str:
        """Selected all message."""
        return "You have selected all the past questions."

    def selected_index_message(self, index: int) -> str:
        """Selected index message."""
        return f"You have selected past question #{index}."

    def not_enough_balance_message(self, balance: int, length: int) -> str:
        """Not enough balance message."""
        return f"You don't have enough balance to download {length} past questions. You have {balance} past questions left. You can top up with /subscribe. Tap on /subscription to view the subscription plans."

    def failed_to_register_account_message(self) -> str:
        """Failed to register account message."""
        return """Failed to register your account, please try again later."""

    def generic_error_message(self) -> str:
        """Generic error message."""
        return """Sorry, there was a problem processing your request."""

    def error_message_to_user_message(self) -> str:
        """Error message to user message."""
        return "Sorry, an error occurred. Please try again later."

    def format_error_message_to_admin(
        self, exception: Exception, user_id: str, username: str, last_message: str
    ) -> str:
        """Format error message to admin."""
        error_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # traceback_details = "".join(traceback.format_exception(exception))

        error_message = f"""Error occurred:
    Timestamp: {error_timestamp}
    User ID: {user_id}
    Username: @{username}
    Last Message: {last_message or 'N/A'}

    The type of error: {type(exception).__name__}
    The error message: {str(exception)}
    """
        return error_message
