# Implementation of a TreeNode class to build our tree
class TreeNode:
    def __init__(self, text):
        self.text = text
        self.children = []

    def add_child(self, Node):
        self.children.append(Node)


with open('./Greenville-Ordinance/Ordinance.txt', 'r') as f:
    root = TreeNode("Ordinance")
    text = f.read()
    sections = text.split("\n\n\n\n")
    sub_sections_list = []
    sub_section_with_description_list = []
    sub_sub_sub_sections_list = []
    for section in sections:
        sub_sections = section.strip().split('-' * 50)
        sub_sections_list.append(sub_sections)
        for sub_section in sub_sections:
            sub_sub_sections = sub_section.strip().split('\n\n')
            sub_section_with_description_list.append(sub_sub_sections)
            for sub_sub_sub_section in sub_sub_sections:
                sub_sub_sub_sections_list.append(sub_sub_sub_section.strip())