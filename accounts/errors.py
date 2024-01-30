def serialer_error(errors:dict)->dict:
    error_response={}
    for key,value in errors.items():
        msg=value[0]
        error_response[key]=str(msg)
    return error_response