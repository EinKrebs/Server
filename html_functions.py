def base_structure(title, content):
    return ('<!DOCTYPE html>\n' 
            '<html>\n'
            '<head>'
            f'<title>{title}</title>\n'
            '</head>\n'
            '<body>\n'
            f'{content}'
            '</body>\n'
            '</html>')


def block(elem_name, content):
    return f'<{elem_name}>\n{content}\n</{elem_name}>\n'
