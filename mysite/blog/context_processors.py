

def groups_context_processor(request):
    return {'user_groups': request.user_groups}
