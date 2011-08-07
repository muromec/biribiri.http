from werkzeug.wrappers import Request, Response
from biribiri import chain

def page(upd_ctx, **ctx):
    return upd_ctx.update({
            "content": "Ya here!",
    })

def title(upd_ctx, **ctx):
    return upd_ctx.update({
            "title": "Herou worudo111",
        })

def render(upd_ctx, **ctx):
    upd_ctx['content_type'] = 'text/html'

    return """
<html>
    <head>
        <title>%(title)s</title>
    </head>
    <body>
        <h1>%(title)s</h1>
        %(content)s
    </body>
</html>""" % ctx

def route(request, **ctx):

    if request.url.startswith('/static/'):
        return

    return [render, title, page]

@Request.application
def entry(request):

    ret = chain.run([route], request=request)
    body = ret.get('render')
    content_type = ret.get('content_type')
    
    return Response(body, content_type=content_type)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, entry)
