from functools import wraps
from flask import flash, render_template, has_request_context


def handleError(error_message="Something went wrong", log_trace=True, internal_error=0):
    """
    Decorator to wrap functions with error handling.

    - error_message: Message shown to user
    - log_trace: Whether to print full traceback in console
    - internal_error: 1 = hide internal data from user (production-safe)
                      0 = show exception details
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Print traceback in console
                if log_trace:
                    import traceback
                    print(f"\n[ERROR] Function: {func.__name__}")
                    print(f"Exception: {e}")
                    traceback.print_exc()
                    print("\n")

                # Prepare message for user
                user_message = error_message
                if internal_error == 0:
                    user_message = f"{error_message}: {str(e)}"

                # Flash message if inside Flask request context
                if has_request_context():
                    flash(user_message, "error")
                    # Try rendering error page only if internal_error=0
                    if internal_error == 0:
                        try:
                            return render_template("error.html", error_message=user_message)
                        except RuntimeError:
                            pass  # fallback if template can't be rendered

                # Return None otherwise
                return None

        return wrapper
    return decorator
