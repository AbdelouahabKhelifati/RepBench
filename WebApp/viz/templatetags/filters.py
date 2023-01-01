from django import template
from WebApp.viz.catch22.features import features
register = template.Library()





## catch22 filters
paper_link = "https://www.biorxiv.org/content/10.1101/532259v1.full.pdf"
@register.filter()
def c22_description(feature_name):
    return features[feature_name]["description"]

@register.filter()
def cc2_paper_link():
    return paper_link

@register.filter()
def c22_abr(feature_name):
    return features[feature_name]["abr"]