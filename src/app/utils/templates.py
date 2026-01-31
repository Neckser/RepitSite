def verstkaprofile(file, name, first_name, last_name):
    formatted_content = file.replace("{{ name }}", name)
    formatted_content = formatted_content.replace("{{ first_name }}", first_name)
    formatted_content = formatted_content.replace("{{ last_name }}", last_name)
    formatted_content = formatted_content.replace("{{ avatar }}", first_name[0] + last_name[0])
    
    return formatted_content