# -*- coding: utf-8 -*-

def writeStyle(col):
    # if col == 'doi':
    #     hrf = 'https://doi.org/'+dataframe.iloc[i][col]
    #     return html.A([dataframe.iloc[i][col]], href=hrf, target="_blank")
    # else:
    #     return dataframe.iloc[i][col]
    if col == 'task':
        return {'minWidth': '200px', 'width': '200px', 'maxWidth': '200px'}
    else:
        return {}