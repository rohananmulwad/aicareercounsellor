from functools import wraps
from flask import flash,render_template

def handleError(error_message="something went wrong",log_trace=True,internal_error=0):
     """
    Decorator to wrap functions with error handling.

    - error_message: Message shown to user
    - log_trace: Whether to print full traceback in console
    - internal_error: 1 = hide internal data from user (production-safe), 0 = show exception
    """
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as e:
                if log_trace:
                    import traceback
                    print(f"\n[ERROR] Function :{func.__name__}")
                    print(f"Exception : {e}")
                    print("Traceback:")
                    traceback.print_exc()
                    print("\n")
                    
                user_message=error_message
                if internal_error==0:
                    user_message=f"{error_message}:{str(e)}"
                    flash(user_message,"error")
                    try:
                        return render_template("error.html",error_message=user_message)
                    except RuntimeError:
                        return None
        return wrapper
    return decorator