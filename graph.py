#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats

#now get response speeds for each descriptor
#measures ease of response to each descriptor
#first/time+second/time...
def getCombinedMetric(data):
    times = {}
    scores = {}
    firsts = {}
    for trial in data:
        score = 0
        d = trial["descriptor"]
        if(d=="null"):
            continue
        if(d=="awake"):
            d = "awake, day"
        if trial["responses"] != "":
            rtList = list(map(float, trial["rt"].split(",")))
            score = sum([(1000/rt) for rt in rtList])
        scores[d] = scores.get(d, [0,0])
        scores[d][0] = scores[d][0] + score
        scores[d][1] = scores[d][1] + 1
        if(trial["q_order"]==1):
            firsts[d] = firsts.get(d, [])
            firsts[d].append(score)
    combined = {}
    for d in scores.keys():
        combined[d] = scores[d][0]/scores[d][1]
    return combined





def get_pred_and_ease(cat, col):
    #plot histogram of original generations, full hist to show response distrib and then just top? with like a magnifying glass think
    if cat not in ['sports', 'kitchen']:
        cat_str = cat[:-1]
    else:
        cat_str = cat
    with open('item-generations/generation_data_clean/' + cat_str + '_counts.json') as f:
        genCounts = json.load(f)
    
    
    #plot generations
    bottom = list(genCounts.items())[-10:]
    bottom_labels = [pair[0] for pair in bottom]
    bottom_data = [pair[1] for pair in bottom]
    top = sorted(genCounts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_labels = [pair[0] for pair in top]
    top_data = [pair[1] for pair in top]
    labels = top_labels + ['','',''] + bottom_labels
    data = top_data + [0,0,0] + bottom_data
    for i in range(len(labels)):
        if labels[i]=='grizzly bear':
            labels[i] = 'bear'

    pos = range(len(data))
    fig = plt.figure(figsize = (10, 5))
    plt.bar(pos, data)
    plt.xticks(pos, labels, rotation=40)
    plt.show()
    
    
    """
    g = sorted(genCounts.items(), key=lambda x: x[1], reverse=True)
    g_labels = [pair[0] for pair in g]
    g_data = [pair[1] for pair in g]
    g_pos = range(len(g_data))
    fig = plt.figure(figsize = (10, 5))
    plt.bar(g_pos, g_data)
    #plt.xticks(g_pos, g_labels, rotation=90)
    #ax = plt.axes()
    #plt.axes().set_ylabel('Response Frequency', fontweight='bold')
    #plt.show()
    """


    #get ratings
    with open('item-ratings/descriptor-ratings/' + cat + '.json') as f:
        ratings = json.load(f)
    descriptors = list(ratings.keys())

    #plot zoo animals in 3d space - large, cute, dangerous?
    """
    descriptors = ['cute', 'large', 'dangerous']
    animals = ['lion', 'elephant', 'penguin', 'snake', 'goat', 'beetle']
    large,cute,dangerous=[],[],[]
    for an in animals:
        large.append(ratings['large'][an])
        cute.append(ratings['cute'][an])
        dangerous.append(ratings['dangerous'][an])

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('cute', fontweight='bold')
    ax.set_ylabel('large', fontweight='bold')
    ax.set_zlabel('dangerous', fontweight='bold')
    ax.set_zlim([1,5])
    for i, an in enumerate(animals):
        ax.text(cute[i], large[i], dangerous[i], an + '\n', fontweight='bold')
    for i, an in enumerate(animals):
        ax.text(cute[i], large[i], dangerous[i], ' (' + str(round(cute[i],2)) + ',' + str(round(large[i],2)) + ',' + str(round(dangerous[i],2)) + ')')
    ax.scatter3D(cute, large, dangerous)
    plt.xlim([1,5])
    plt.ylim([1,5])
    plt.locator_params(axis="x", nbins=5)
    plt.locator_params(axis="y", nbins=5)
    plt.locator_params(axis="z", nbins=5)
    plt.show() 
    """

    #all items for this cat with data
    with open('item-generations/item-lists/' + cat + '.json') as f:
        animals = json.load(f)
    animals = [a.lower() for a in animals]
    rm=[]
    for a in animals:
        if a not in genCounts.keys():
            genCounts[a] = 0
        if a not in ratings[list(ratings.keys())[0]]:
            rm.append(a)
    for r in rm:
        animals.remove(r)
    

    #linear regression between descriptor scores for animals and animals' likelihood of coming to mind
    """
    genCounts['beetle'] = 0
    genCounts['mouse'] = 0
    genCounts['tarantula'] = 0
    genCounts['cow'] = 0

    #x_i is for each animal, rating for descriptor_i
    des_ratings = []
    for a in animals:
        an_list = []
        for des in descriptors:
            an_list.append(ratings[des][a])
        des_ratings.append(an_list)
    x = np.array(des_ratings)

    #y is for each animal, likelihood of coming to mind (aka generation counts)
    y = np.array([genCounts[a]/num_gen for a in animals])

    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    b0 = model.intercept_
    b1 = model.coef_
    print(r_sq)
    print(b0)
    for i in range(len(b1)):
        print(descriptors[i] + ': ' + str(b1[i]))
    """

    #now let's get correlations of each feature with generation counts
    animal_counts = [genCounts[a] for a in animals]
    des_gen_corrs = {}
    for d in descriptors:
        d_scores = []
        for a in animals:
            d_scores.append(ratings[d][a])
        des_gen_corrs[d] = np.corrcoef(animal_counts, d_scores)[0][1]
    #now lets plot a bar graph
    corrs = sorted(des_gen_corrs.items(), key=lambda x: abs(x[1]), reverse=True)

    corrs_labels = [pair[0] for pair in corrs]
    """
    corrs_labels = ['striking', 'large', 'dangerous', 'long lifespan', 'cool', 'carnivore', 'quiet', 'mammal', 'normal', 'omnivore', 'invertibrate', 'lives on land', 'bird', 'think of often', 'long hair', 'lives in water', 'herbivore', 'amphibean', 'large feet', 'lives in desert', 'good hearing', 'nocturnal', 'diurnal', 'fish', 'cute', 'sleeps very little', 'lives in tropics', 'reptile', 'lives in forest', 'lives in arctic']
    
    for i, l in enumerate(corrs_labels):
        if l in ['tropics', 'forest', 'desert', 'land', 'water']:
            corrs_labels[i] = '(lives) ' + l
        else if l in ['diet, carnivore', 'diet, omnivore', 'diet, herbivore']:
            corrs_labels[i] = l[6:]
        else if l in ['type, mammal', 'type, invertibrate', 'type, bird', 'type, amphibean']
    
    corrs_data = [abs(pair[1]) for pair in corrs]
    corrs_pos = range(len(corrs_data))
    fig = plt.figure(figsize = (10, 5))
    plt.autoscale()
    cols=[]
    for c in corrs:
        if c[1]>0:
            cols.append('blue')
        else:
            cols.append('red')
    plt.bar(corrs_pos, corrs_data, color = cols)
    plt.xticks(corrs_pos, corrs_labels, rotation=50, ha='right')
    plt.ylabel('Predictiveness of Coming to Mind', fontweight='bold')
    plt.subplots_adjust(bottom=0.21)
    plt.show()
    """
    #responses to timed trials

    with open('timed-item-generations/response_data/' + cat + '.json') as f:
        timed_responses = json.load(f)
    
    #ease of response for each feature
    timed_scores = getCombinedMetric(timed_responses)
    """
    #plot ease of response
    scores = sorted(timed_scores.items(), key=lambda x: abs(x[1]), reverse=True)
    scores_labels = [pair[0] for pair in scores]
    scores_labels = ['dangerous', 'normal', 'cool', 'carnivore', 'large', 'lives on land', 'striking', 'diurnal', 'think of often', 'cute', 'mammal', 'good hearing', 'long lifespan', 'quiet', 'lives in tropics', 'large feet', 'long hair', 'sleeps very little']
    scores_data = [abs(pair[1])/max(timed_scores.values()) for pair in scores]
    scores_pos = range(len(scores_data))
    fig = plt.figure(figsize = (10, 5))
    plt.bar(scores_pos, scores_data)
    plt.xticks(scores_pos, scores_labels, rotation=50, ha='right')
    plt.ylabel('Feature Relevance', fontweight='bold')
    plt.subplots_adjust(bottom=0.21)
    plt.show()
    """
    
    #correlation between ease of response and predictiveness of coming to mind
    p,e=[],[]
    print(cat)
    if cat=='animals':
        des = ['dangerous', 'normal', 'cool', 'carnivore', 'large', 'lives on land', 'striking', 'diurnal', 'think of often', 'cute', 'mammal', 'good hearing', 'long lifespan', 'quiet', 'lives in tropics', 'large feet', 'long hair', 'sleeps very little']
        des2 = ['dangerous', 'normal', 'cool', 'diet, carnivore', 'large', 'land', 'striking', 'awake, day', 'think', 'cute', 'type, mammal', 'has good hearing', 'lifespan', 'quiet', 'tropics', 'has large feet relative to its body size', 'has long hair', 'sleeps very little']
    else:
        des = list(timed_scores.keys())
        des2 = des
    des3 = []
    for d in des2:
        if(des_gen_corrs[d]>0):
            continue
        print(d)
        e.append(timed_scores[d]/max(list(timed_scores.values())))
        p.append(abs(des_gen_corrs[d]))
        des3.append(d)
    print(np.corrcoef(e, p)[0][1])
    #cor, pval = stats.pearsonr(e,p)
    #print(cor)
    #print(pval)
    
    #now plot

    #labels
    #if len(p) < 1:
    #    return p, e, des3
    """
    for i, d in enumerate(des3):
         ax.text(p[i], e[i], ' ' + d, color=col)
    #points
    plt.scatter(p, e, color=col)
    #label axes
    plt.xlabel('Predictiveness of Coming to Mind', fontweight='bold')
    plt.ylabel('Ease of Response', fontweight='bold')
    p1 = np.polyfit(p, e, 1)
    #xlims = plt.xlim()
    #p.insert(0, xlims[0])
    #e.insert(0, np.polyval(p1, xlims[0]))
    #p.append(xlims[1])
    #e.append(np.polyval(p1, xlims[1]))
    #if cat=='animals': cat = 'zoo animals'
    #elif cat=='kitchen': cat = 'kitchen appliances'
    #elif cat=='restaurants': cat = 'chain restaurants'
    plt.plot(p, np.polyval(p1,p), linewidth = 1.5, color=col, label=cat)
    #plt.xlim(xlims)
    """

    """
    print(cat)
    print(np.corrcoef(e, p)[0][1])
    print('_____________________')
    print(p)
    print('_____________________')
    print(e)
    print('_____________________')
    print(des)
    print('_____________________')
    """
    return p, e, des3
    


#now plot, for each category, ease of response vs predictiveness for each feature

#fig = plt.figure()
#ax = plt.axes()
#ax.set_xlabel('Predictiveness of Coming to Mind', fontweight='bold')
#ax.set_ylabel('Ease of Response', fontweight='bold')

#add each category
colors = ['red', 'blue', 'green', 'orange', 'pink', 'purple', 'black']
c=0
cat_dict = {}
#fig = plt.figure()
#ax = plt.axes()
categories = ['animals', 'kitchen', 'restaurants',  'vegetables', 'holidays', 'jobs', 'sports'] #['vegetables', 'animals', 'jobs', 'restaurants', 'sports']#
allx = []
ally = []
for cat in categories:
    cat_dict[cat] = {}
    p,e,des = get_pred_and_ease(cat, colors[c])
    allx = allx + p
    ally = ally + e
    c=c+1
    #cat_dict[cat]['pred'] = p
    #cat_dict[cat]['ease'] = e
    #cat_dict[cat]['des'] = des
    #cat_dict[cat]['col'] = [colors[c] for j in range(len(p))]
    #c=c+1
#plt.legend()
#plt.show()

#print(np.corrcoef(allx, ally)[0][1])
cor, pval = stats.pearsonr(allx, ally)
print(cor)
print(pval)
#2.3582398802254628e-09
#0.5676081492985638
#if we take abs of all negatives:          0.607174156451246, an: 0.553, veg: 0.894, res: 0.911
#if we take abs of just strong negatives:  0.607174156451246,  an: 0.553, veg:0.894, res: 0.911
#if we take abs of just weak negatives:    0.6063283680583847, an: 0.356, veg: 0.880, res: 0.851
#if we don't take abs value at all:        0.6176930723260331, an: 0.399, veg: 0.898, res: 0.850
#relationship virtually unchanged when we take the absolute value vs not over all categories
#only 4 strong negatives (1 in restaurants, 1 in vegetables, 2 in animals)
#looking only at the negatives, over all still pos relationship (tho slight) (0.1386424404042517)
#restaurants 0.681435657729446 (3) vegetables -0.48741033171337056 animals 0.6373726901968907 - each have 3
#

"""
    for i, d in enumerate(des):
        ax.text(p[i], e[i], d)

    ax.scatter(p, e, color=colors[c])

    #obtain m (slope) and b(intercept) of linear regression line
    m,b = np.polyfit(p, e, 1)
    #add linear regression line to scatterplot 
    ax.plot(p, [m*p_var+b for p_var in p],  color=colors[c])
    c=c+1
"""

"""
vegetables
0.8944783675538271
animals
0.5530131721778706
holidays
0.7476336877549481
jobs
0.277288999880707
kitchen
0.38952366926608023
restaurants
0.9107391253240134
sports
0.6750071109467219
"""

#show r value overall ()
#do for each, then list each individually (interested in variation across categories, )
#0.607174156451246
#0.5676081492985636