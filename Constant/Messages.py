# importing enum for enumerations
import enum
'''
Python Flask  API
Developed By : Mandeep Singh
'''
# creating enumerations using class
class Messages(enum.Enum):

    SOME_WENT_WRONG = "Something went wrong, Please try again!"
    EXECUTION_SUCCESSFULLY = "Execution Successfully"
    NOT_FOUND_YOUR_REQUEST = "Not found your request"
    TYPE_NOT_ALLOWED = "This method is not allowed for the request"
    INTERNAL_SERVER_ISSUE = "Issue From Internal Server"
    TOKEN_EXPIRED = "User Token Expired, please login again"

    ''' Authentication Module Message'''
    WELCOME_AUTH_HOME = "Welcome in Authentication Module"
    INVALID_OTP = "Entered OTP code is invalid"
    RESEND_OTP = "Otp sent"
    SEND_OTP = "Otp sent to your entered phone number"
    PROFILE_UPDATE = "Profile updated"
    ALREADY_EMAIL_ID_EXIST = "User already registered using this Email Id."
    ALREADY_PHONE_NUM_EXIST = "User already registered using this Phone Number."

    ''' Note Module Message'''
    WELCOME_NOTE_HOME = "Welcome in notebook module"
    NOTE_ADDED_IN_NOTEBOOK = "Note added in your noteBook"
    NOTE_UPDATE_IN_NOTEBOOK = "Note updated in your noteBook"
    NOTE_NOT_UPDATE = "Note not updated "
    NOTE_ALREADY_EXISTING = "Note already exist in notebook"
    NOTE_DELETE = "Note delete from notebook"
