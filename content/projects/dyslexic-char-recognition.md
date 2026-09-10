---
Title: Dyslexic Character Recognition
Slug: dyslexic-char-recognition
Project Type: University Project
Duration: Sep 2022 - Nov 2022
Summary: Developed a deep learning-based system to recognize handwritten characters by individuals with dyslexia or dysgraphia (affecting 9-12% of population).
Skills: Convolutional Neural Networks (CNN) · TensorFlow · Python
Image: dyslexic-char-recognition.jpg
Order: 3
---

<h2 id="overview">Overview</h2>
<p>Developed a deep learning-based system to recognize handwritten characters by individuals with dyslexia or dysgraphia (affecting 9-12% of population).  </p>
<h2 id="highlights">Highlights</h2>
<ul>
<li>Used CNN models combined with mathematical algorithms for recognition.  </li>
<li>PCA and K-Fold cross-validation achieved highest accuracy: 90.04%.  </li>
</ul>
<h2 id="repository">Repository</h2>
<p><a href="https://github.com/shrishtinigam/dyslexic-character-recognition">dyslexic-character-recognition - GitHub Link</a></p>
<h1 id="dyslexic-character-recognition">Dyslexic Character Recognition</h1>
<p>In this paper, we implement a CNN model to recognize and rectify incorrectly written characters, in order to aid children with dysgraphia as a result of dyslexia. Dysgraphia is a language disorder that is defined as a difficulty or inability to coherently communicate through writing. The proposed work attempts to implement a CNN classification model that categorizes a character as correctly written or incorrectly written, and if it is incorrectly written, identifies the character it was supposed to be. Our goal is to aid children with writing difficulties to practice their writing with the model helping them correct their mistakes. Compared to the conventional testing procedures that take in a lot of time in screening, an automated detection mechanism would take lesser time and produce reliable results while analyzing the writing aspect.</p>
<h1 id="dataset">Dataset</h1>
<p>Dataset was collected from 3 sources where uppercase letter is from NIST Special Database 19 while lowercase letter is from Kaggle Dataset and some datasets for testing is from dyslexic kids of Seberang Jaya primary school, Penang, Malaysia. This dataset contains a total of 78275 for normal class while for reversal is 52196 and for corrected is 8029.</p>
<h1 id="proposed-methodology">Proposed Methodology</h1>
<p>In our work, we show a comparative analysis between various perceptron and CNN based learning methods to recognize reversed characters. We first apply a CNN model for the binary classification of reversed characters and regular characters as below. Label 0 is assigned to Normal characters, and Label 1 is assigned to reversed characters. Next, we use a Multi-Layer Perceptron to recognize the reversed and normal characters. 0-25 Labels are assigned to normal characters. 26-51 labels are assigned to reversed characters. Some reversal mistakes are common, for example, vertical flip of asymmetrical letters like B, K, F etc. Some letters however, are symmetrical, like A, O etc., and thus have no reversal character equivalents. Such letters, in total are – A, H, M, O, V, W, X, Y. This dataset is applied to the rest of the methodologies as well.</p>
<h1 id="results">Results</h1>
<p>Maximum accuracy reached was 90.4% by the Character Recognition K-Fold Cross Validation Larger CNN model. Comparision between all the models implemented is shown below.</p>
<table border="1" cellspacing="0" cellpadding="5">
  <caption>
    <em>Table: Accuracy, Precision, Recall, F1-Score Achieved by Different Models and Their Run-Times.</em>
  </caption>
  <tr>
    <th>Model \ Parameters</th>
    <th>Accuracy</th>
    <th>Precision</th>
    <th>Recall</th>
    <th>F1-Score</th>
    <th>Run-Time of Model Training</th>
  </tr>
  <tr>
    <td>Binary Classification CNN</td>
    <td>82.6</td>
    <td>75.2</td>
    <td>80.4</td>
    <td>78.8</td>
    <td>1 Minute</td>
  </tr>
  <tr>
    <td>Character Recognition MLP</td>
    <td>86.3</td>
    <td>86.3</td>
    <td>86.3</td>
    <td>86.3</td>
    <td>2.33 Minutes</td>
  </tr>
  <tr>
    <td>Character Recognition CNN</td>
    <td>84.7</td>
    <td>84.7</td>
    <td>84.7</td>
    <td>84.7</td>
    <td>5 Minutes</td>
  </tr>
  <tr>
    <td>Character Recognition Larger CNN</td>
    <td>87.9</td>
    <td>87.9</td>
    <td>87.9</td>
    <td>87.9</td>
    <td>7 Minutes</td>
  </tr>
  <tr>
    <td>Character Recognition K-Fold Cross Validation Larger CNN</td>
    <td>90.4</td>
    <td>90.4</td>
    <td>90.4</td>
    <td>90.4</td>
    <td>35 Minutes</td>
  </tr>
</table>

<p>Comparision to various other existing models is shown in the following table. As shown, our model shows comparative accuracy.</p>
<table border="1" cellspacing="0" cellpadding="5">
  <tr>
    <th>Index</th>
    <th>Model Name</th>
    <th>Model Accuracies</th>
  </tr>
  <tr>
    <td>1</td>
    <td>I - ANN Model</td>
    <td>73.33</td>
  </tr>
  <tr>
    <td>2</td>
    <td>III - CNN on EOG Signals</td>
    <td>80.94</td>
  </tr>
  <tr>
    <td>3</td>
    <td>VII - CNN Model</td>
    <td>92.4</td>
  </tr>
  <tr>
    <td>4</td>
    <td>VII - NDR-R2CNN Model</td>
    <td>96.5</td>
  </tr>
  <tr>
    <td>5</td>
    <td>VIII - SVM</td>
    <td>85.055</td>
  </tr>
  <tr>
    <td>6</td>
    <td>XI - Random Forest and DL</td>
    <td>55.7</td>
  </tr>
  <tr>
    <td>7</td>
    <td>XII - CNN</td>
    <td>87.44</td>
  </tr>
  <tr>
    <td>8</td>
    <td>XIV - SVM</td>
    <td>94.5</td>
  </tr>
  <tr>
    <td>9</td>
    <td>XV - CNN-SVM</td>
    <td>94.4</td>
  </tr>
  <tr>
    <td>10</td>
    <td>Our Larger CNN Model</td>
    <td>90.4</td>
  </tr>
</table>
