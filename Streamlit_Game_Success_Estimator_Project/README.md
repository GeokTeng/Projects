<img src="http://imgur.com/1ZcRyrc.png" style="float: left; margin: 20px; height: 55px">

# Streamlit Game Success Estimator
---
This is an overview of the project.

**Notebooks**<br>
01_DataCollection<br>
02_DataCleaning_EDA<br>
03_BaselineModel<br>
04_Improved_Model<br>

# Introduction:

***Problem statement***:<br>
It is not unknown of that investment is a balance of risk and benefit. In the gaming industry, it is very dynamic and maybe challenging to determine is a game is worth investing in. As such, we aim to create a classification model that will improve investment chance of successful investment in  pre-released or early-accessed games by looking into the <code>game's description</code>.

We look at a <code>'Good Game'</code> or  *'Successful' game*: a game well received by users, in other words, games which received largely positive reviews. 

So our main focused feature is the <code>game description</code>, and our target variable is whether a game is a <code>'Good Game'</code>.

The model performance will be compared and assessed against the investment chance of investing in a successful game without using the model (default probability = percentage of defined 'Successful' games in the dataset). As such, our main assessment metrics of the model is it's <code>**precision**</code>.

Our focused and dataset will be on the games from [*Steam*](https://store.steampowered.com/). However, we would wish for the model to be applicable to other game websites/platforms as well.

# Data Collection, Proccessing and Analysis:

|Phase|Process involved|Remarks|
|---|---|---|
|Data Collection|<br><li>Beautiful Soup</li><li>Selenium</li>|50k rows with 7 columns:<br><br><li>Title</li><li>Url</li><li>Review</li><li>Game Description</li><li>User-defined tags</li><li>Released date</li><li>Price</li>|
|Data Cleaning|Check and address if necessary:<br><li>Missing Data</li><li>Duplicate Data</li><li>Unhelpful data (e.g. Games with no reviews)</li><li>Data types</li><li>Outliers</li>|Data collected contain 50K data rows and 7 columns.Resulting datadframe after cleaning has 49+K data rows and 7 columns.|
|Data Processing|**Review-related columns**<br><br>Extracting numerical data from the information in 'Review', such as *Total Reviews* and *Percentage of positive reviews* and creating new feature columns|Some games do not have reviews or have insufficient reviews to be given a 'review type' (*Positively, Mixed or Negatively reviewed*)<br><br> Such games are dropped, resulting dataframe with 27+K data rows and 10 columns.|
|Target variable column: <code>Good Games</code>|**Good Game or Poor Game**<br><br>We followed how *Steam* labelled a game as postive review type; games that are classified as 'Positive' reviewed are the games with at least 70% of postive reviews. Such game are classified as 'Good' game, else they are 'Poor' games.| Resulting dataframe contains 27+K data rows and 11 columns.|
|EDA|<li>Correlation analysis</li><li>Distribution</li>|Some key findings from EDA:<br><br><li>**About 72% of the games are 'Good' games. </li><li>As such, <code>our model aims to give precision much higher than 72%.**</code></li><li>A correlation anlysis there does not appear an obvious correlation between price, total reviews and year of game release to the percentage of positive reviews.</li><li> Majority of the games were released from 2017 onwards. Possibly this was the year where Steam has been more actively recorded game data.</li><li>The games generally received 60% positive reviews.</li><li>About 75% of the games have 90 or less number of reviews</li>|

# Baseline Model (Preprocessing, modelling, evaluation)

**Process involved**:
>CountVectorizer(stop_words = 'english',max_features=1500)

**Model used**:
>Random Forest

**Performance**:
> ![](images/baseline_model_metrics.jpg)

**Comments**:

In the interest of answering our business problem, our focus is mainly on precision (% of True 'Good Games' among those who are predicted to be 'Good Games'.)
- While the model has good recall(0.99), it has poor precision (precision = 79% VS 72% actual 'Good Games' in the test set).
- This will does somewhat well for our stakeholder, as the chances of them obtaining a 'Good Game' did increased by 7% with the use of the model.

**How are we going to improve model's performance?**
1. Explore using different choice of model (e.g. Random Forest)
1. Include Stemming/Lemitisation during preprocessing
1. Apply conditions such as *min_df* and *max_df* during vectorisation
1. Attempt using TFIDF vs CountVectorizer
1. Attempt searching for Bigrams

# Approach 1: Explore Random Forests¶

**Process involved**:
>CountVectorizer(stop_words = 'english',max_features=1500)

**Model used**:
>RandomForestClassifier(max_depth=50)

**Performance**:
> ![modelA_performance](images/modelA_metrics.jpg)

**Comments:**

Random Forest appeat to give poorer model performance compared to our baseline model (Multinomial Naive Bayes(MNB)).
- It has a precision score of 0.73 (vs 0.79).

> Let's further improve the performance of MNB by trying different vectorizers to select the terms used for modelling. 

# Approach 2: Explore different Vectorizers and parameters
Note: From this approach onwards, we are working on game description after applying <code>stemming</code>

**Process involved**:
> ![diff_vect](images/diff_vect.jpg)

**Model used**:
>Multinomial Naive Bayes

**Performance**:
> ![diff_vect_precision](images/diff_vect_precision.jpg)

**Comments:**

These precision scores are poorer than that in the earlier model in Approach A (0.79), indicating possible high false Negative, which is not desirable to our stakeholders.

# Approach 3:  Explore different vectorizers with game with at least 50 reviews
**Rationale**:<br> Good Games are defined as games with more than 70% positive reviews. However, there are games with small number of reviews, raising concern whether labelling as such is accurate. 

> We shall now explore how the model (MNB) perform when we only include games with minimum 50 reviews.
> With smaller dataset, we are able to expand our max_features to a larger number while still performing within our computer's limit.


**Note: New Precision Target**
- Now that we filter out games with <50 reviews, the new sample have 77.6% 'Good Games'.
- Now, in other words, the model has to aim for precision much better than 77.6%

### Let's look at the descriptive statistics of the number of reviews a game receives: 
![review_stats](images/total_reviews_stats.jpg)<br>
![chart1](images/total_reviews_chart.jpg)


### Approach 3 Modelling
**Process involved**:
> ![diff_vect2](images/diff_vect2.jpg)

**Model used**:
>Multinomial Naive Bayes

**Performance**:
> ![diff_vect_precision](images/diff_vect_precision2.jpg)

**Comments**<br><br>
CountVectorizer generally performed better than TFIDFVectorizer.

Using **cvec_uniG_biG** seemed to gave the best precision score of 0.83. 
> However the improvement from 0.77 seems to be lesser thant the improvement in the initial Naive Bayes model (from 0.72 to 0.79).

![modelC](images/modelC_metrics.jpg)modelC_metrics

# Approach 4: Selecting NGrams terms found in Games Descriptions

The aim is to filter out NGrams that are commonly found in 'Good' and 'Poor' games'.
> By doing so, we hope to improve model ability to differentiate 'Good' and 'Poor' game.
> Note at this point we are still using the games_atlst50revw_df(games with minimum 50 reviews)

**How is this done?**
> - Firstly, we obtain top 100 Unigrams, Bigrams and Trigrams in 'Good' and 'Poor' games
> - Next, we identify common unigrams/bigrams/trigrams between the 'Good' game set and 'Poor' game set of terms.
> - Together, this set of common unigrams/bigrams/trigrams will form the set **target_grams** (396 terms) which will be used to exlude feature columns after vectorising


**Process involved**:
> ![_vectD](images/vect_approachD.jpg)

**Model used**:
>Multinomial Naive Bayes<br>
>Data used for train_test: Subset data(games with minimum 50 reviews, sample size =10+K)<br>
>Precision score to beat: 0.77

**Performance**:
> ![modelD](images/modelD_metrics.jpg)modelD_part2_metrics

**Comments**<br><br>
Compared to baseline MNB using cvec_uniG_biG (precision 0.83, recall 0.76, specificity 0.48), this new approach, the model has same precision score, while having higher recall and poorer specificity (precision 0.83, recall 0.81, specificity 0.45).

> Overall, the improvement in True positive is much greater than the decline in specificity for True negative. As such, this model is more favoured to be used for addressing our business problem.

## Exploring the approach with full data set
**Model used**:
> Multinomial Naive Bayes<br>
> Data used for train_test: base dataset(sample size = 27+K)<br>
> Precision score to beat: 0.72

**Performance**:
> ![modelD2](images/modelD_part2_metrics.jpg)

**Comments**:
> Comparing the model performance to that inital of the Naive Bayes model at the beginning of this notebook, our latest model performed well with higher precision (0.80 vs 0.79), higher True Positive (3752 vs 3733) and Lower False Positive (963 vs 1018)! 

# Approach 5: Let's further explore Approach 4 onto few other models
- We tried on a few other classification models (e.g. KNeighbours Classifier, Log Regression, RandomForest and Complement Naive Bayes).
- Complement Naive Bayes shown based performance
## Use Complement Naive Bayes
> CNB has improved accuracy compared to standard NB, especially when the class distribution is imbalanced (i.e. when one class has significantly more instances than another).

**Model used**:
> Complement Naive Bayes (alpha=0.01)<br>
> Data used for train_test: base dataset(sample size = 27+K)<br>
> Precision score to beat: 0.72

**Performance**:
> ![model_best](images/bestmodel_metrics.jpg)

**Comments**:
> Our latest model C_nb = ComplementNB(alpha=0.01), seemed to have the greatest performance! With precision of 0.81, recall of 0.71 and specificity of 0.57.

# Summary

Here is a summary of the key models we have in this project:
> The summary present model performance on the sample data **without filtering games by their number of reviews (n = 27309).**

|Model|Description|Performance|
|---|---|---|
|Baseline Model<br>Random Forest|<li>CountVectorizer (include stopwords = english, unigram, maxfeatures:1500)</li>|<li>Precision:0.73</li><li>Recall: 0.99</li><li>Specificity: 0.05</li><li>Comments:<br> Poor improvement from ~72%. Also, it has very high false positive</li>|
|Initial Multinomial Naive Bayes|Using same Count Vectorization setting|<li>Precision:0.79</li><li>Recall: 0.76</li><li>Specificity: 0.47</li><li>Comments:<br> Precision 79% much better improvement compared to baseline.</li>|
|Multinomial Naive Bayes|<li>CountVectorizer <br>(include stopwords = english, unigram, bigram, trigram, maxfeatures:10K)</li><li>Removing terms found in 'target_grams'</li>|<li>Precision:0.80</li><li>Recall: 0.76</li><li>Specificity: 0.49</li><li>Comments:<br> Precision of 80%, better improvement compared to Initial naive bayes (79%).</li>|
|Complement Naive Bayes<br><br>*Ultimately selected model for problem statement*|<li>CountVectorizer <br>(include stopwords = english, unigram, bigram, trigram, maxfeatures:10K)</li><li>Removing terms found in 'target_grams'</li>|<li>Precision:0.81</li><li>Recall: 0.71</li><li>Specificity: 0.57</li><li>Comments:<br> Precision of 81%, better improvement than the use of Multinomial Naive Bayes (80%).</li><li>Notably have much greater specificity than the previous models, which is favoured in the context of our business problem</li>|

# Discusssion and Conclussion:

Our final selected model improve the investors chance of investing in 'Good' games from default probability of 72% to 81%.!

**Limitation**
1. Limited number of reviews (e.g. <50 reviews) may have insufficient to determine if a game is 'Good' or 'Poor'. However, by limiting the dataset to only games with at least a certain number of reviews will significantly reduce the number of available dataset available for analysis and model training.
    - There need to be a balance between the accuracy of labelling a game as 'Good' or 'Poor' and having enough dataset for training model to do differentiate a 'Good' and 'Poor' game.
    - In our final selected model, we worked around this challenge by analysing common terms found in the two classes of games by focusing only on games with at least 50 reviews. We subsequently applied that resulting model approach and target terms filtering on the entire dataset which gave us our best performace.
    - Analysis could have been on comparing the games total number of reviews between correctly and wrong predicted games.
1. Game industry is ever-changing, the model will have to be revised to capture new and upcoming trends.
1. Some features that can greatly determines a game's success may not be captured in the game's description,such as game developers and programmers.
    - such features can be explored and analysed to incorporated to improve model performance.
1. The game has poor specificity (~50%); it is not able to pick up actual poor games well.
    - This is due to lack of information the model needs to identify a game that is actually poor.
    - Features of poor games may be explored and obtained through examining games' negative reviews itself. User's description of why they find a game is 'bad' can give insights on improving the model's ability to detect actual 'True Negatives'
    
**Conclusion**:<br>
Recognising our model's strengths and flaws, what does this mean for our model?<br> What is it place of use in the business context?

> - Investors should use the model to identify potential games for investing while recognising it does not capture other important information making the ultimate call whether a game should be invested or not.
> - The model ultimately narrows down the canditates of games for further consideration for investing, which makes the selection phase much more efficient.
> - While this would mean some opportunity cost (due to False Negative predictions), it is worth noting that it can be overcome by setting a target number of games to invest in, and achieving that target number while being able to save time and resources in the selection and decision making process.