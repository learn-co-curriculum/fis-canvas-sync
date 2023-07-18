import re
import os


"""
This is the script that takes the LaTeX in the readme file and converts it to a github rendered image link.
This method uses Regex for the replacement
The original file will be modified inplace with this script
"""
def latex_to_img(lesson_markdown):
    data = lesson_markdown
    for character in ('$$', '$'):
        sep = character
        sep_clean = sep + " "
        data = re.sub(sep_clean, sep, data)

        if r"\begin{align}" in data:
            re.sub(r'\begin{align}', '&', data)

        if r"\end{align}" in data:
            re.sub(r'\end{align}', '&', data)
        special_characters = ["\\\backslash", "\\\subset", "\\\subseteq", "\\\cap", "\\\cup"]

        data_split = data.split(sep)

        for i in range(len(data_split)):
            if i %2 !=0:
                for item in special_characters:
                    data_split[i] = re.sub(item,(' '+item), data_split[i])
                if "prod" in data_split[i]:
                    data_split[i] = re.sub('prod', 'displaystyle\prod', data_split[i])
                
                if "sum" in data_split[i]:
                    data_split[i] = re.sub('prod', 'displaystyle\sum', data_split[i])
                
                if "+" in data_split[i]:
                    data_split[i] = re.sub('+', '%2b', data_split[i])
                    
                data_split[i] = f' <img src="https://render.githubusercontent.com/render/math?math={data_split[i]}"> '
                # canvas rendering html
                #f"""<img class="equation_image" title="{data_split[i]}" src="https://learning.flatironschool.com/equation_images/{data_split[i]}" alt="LaTeX: p{data_split[i]}" data-equation-content="{data_split[i]}" data-ignore-a11y-check="" />

        data = ''.join(data_split)
    return data
        