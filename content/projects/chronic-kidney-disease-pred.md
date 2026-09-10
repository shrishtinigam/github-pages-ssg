---
Title: Chronic Kidney Disease Prediction using Machine Learning and Deep Learning
Slug: chronic-kidney-disease-pred
Project Type: University Project
Duration: Apr 2022 - Jul 2022
Summary: Performed predictive modeling for Chronic Kidney Disease (CKD) using multiple ML models and CNN on the UCI CKD dataset.
Skills: scikit · TensorFlow · Seaborn · pandas · Python
Image: chronic-kidney-disease-pred.jpg
Order: 4
---

<h2 id="overview">Overview</h2>
<p>Performed predictive modeling for Chronic Kidney Disease (CKD) using multiple ML models and CNN on the UCI CKD dataset.  </p>
<h2 id="highlights">Highlights</h2>
<ul>
<li>Comparative analysis of five ML models and CNN.  </li>
<li>kNN imputation and CNN achieved highest accuracy.  </li>
<li>Extensive exploratory data analysis and pre-processing evaluation.  </li>
<li>CNN achieved <strong>&gt;99% accuracy, precision, recall, and F1-Score</strong> across all datasets.</li>
</ul>
<h2 id="repository">Repository</h2>
<p><a href="https://github.com/shrishtinigam/Chronic-Kidney-Disease-Prediction">Chronic-Kidney-Disease-Prediction - GitHub Link</a></p>
<h1 id="chronic-kidney-disease-prediction-using-machine-learning-and-deep-learning">Chronic Kidney Disease Prediction using Machine Learning and Deep Learning</h1>
<p>Disease prediction is the premier focus of many emerging medical technologies.<br>
Chronic kidney disease (CKD) prediction is a complex task depending mainly on two variables:  </p>
<ul>
<li><strong>Estimated Glomerular Filtration Rate (eGFR / G score)</strong>  </li>
<li><strong>Albumin to Creatinine Ratio (ACR / A score)</strong>  </li>
</ul>
<p>Machine learning techniques (Gaussian Naive Bayes, Logistic Regression, Random Forest, Support Vector Machine, Decision Tree) and deep learning techniques (CNN Sequential model) are applied to predict CKD and classify patients in a binary manner.</p>
<hr>
<h2 id="1-background">1. Background</h2>
<ul>
<li><strong>Definition</strong>: CKD is a sustained reduction in kidney function, leading to permanent and progressive damage.  </li>
<li><strong>Prevalence</strong>: About 800 per million people in India suffer from CKD and 150–200 per million from end-stage renal disease (ESRD) [1].  </li>
<li><strong>Consequences</strong>: CKD may cause waste buildup in the body, kidney failure, and the need for dialysis or transplant.  </li>
<li><strong>Importance of Early Detection</strong>: Early diagnosis allows interventions to protect kidney function.</li>
</ul>
<h2 id="2-domain-knowledge">2. Domain Knowledge</h2>
<ul>
<li><strong>Main Causes</strong>: Diabetic nephropathy, diabetes, hypertension [1,2].  </li>
<li><strong>Risk Factors</strong>: Old age, sex, smoking, nephrotoxic medications [2].  </li>
<li><strong>Symptoms</strong>:  </li>
<li><strong>Asymptomatic stage</strong>: Detected via routine urine and blood tests.  </li>
<li><strong>Early signs</strong>: Hematuria, albuminuria (foamy urine), nocturia, flank pain.  </li>
<li><strong>Advanced stage</strong>: Fatigue, poor appetite, nausea, pruritus, weight loss, dyspnea, edema [3].  </li>
</ul>
<p>Diagnosis criteria:<br>
- eGFR &lt; 60 mL/min/1.73 m² or albuminuria ≥ 30 mg/24 hr for &gt;3 months [3].  </p>
<h2 id="3-complications-quality-of-life">3. Complications &amp; Quality of Life</h2>
<p><strong>Common complications</strong> [2]:<br>
- Anemia<br>
- CKD mineral bone disease<br>
- Cardiovascular disease<br>
- Dialysis-related problems  </p>
<p><strong>Impact on Quality of Life</strong>: Hypertension, fluid retention, bone pain, neuropathy, pruritus, frailty, depression, and medication side-effects.</p>
<h2 id="4-dataset">4. Dataset</h2>
<ul>
<li><strong>Source</strong>: UCI Machine Learning Repository.  </li>
<li><strong>Size</strong>: Data collected over 2 months in India.  </li>
<li><strong>Features</strong>: 25 medical attributes (blood tests, urine tests, demographics).  </li>
<li><strong>Target variable</strong>: Class → <code>ckd</code> / <code>notckd</code>.</li>
</ul>
<h3 id="table-1-dataset-attributes">Table 1: Dataset Attributes</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; text-align: left;">
  <thead>
    <tr>
      <th>Sr. No.</th>
      <th>Attribute Abbr.</th>
      <th>Attribute Name</th>
      <th>Type</th>
      <th>Units</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>age</td><td>Age</td><td>Numerical</td><td>years</td></tr>
    <tr><td>2</td><td>bp</td><td>Blood Pressure</td><td>Numerical</td><td>mm/Hg</td></tr>
    <tr><td>3</td><td>sg</td><td>Specific Gravity</td><td>Nominal</td><td>1.005, 1.010, 1.015, 1.020, 1.025</td></tr>
    <tr><td>4</td><td>al</td><td>Albumin</td><td>Nominal</td><td>0, 1, 2, 3, 4, 5</td></tr>
    <tr><td>5</td><td>su</td><td>Sugar</td><td>Nominal</td><td>0, 1, 2, 3, 4, 5</td></tr>
    <tr><td>6</td><td>rbc</td><td>Red Blood Cells</td><td>Nominal</td><td>normal, abnormal</td></tr>
    <tr><td>7</td><td>pc</td><td>Pus Cell</td><td>Nominal</td><td>normal, abnormal</td></tr>
    <tr><td>8</td><td>pcc</td><td>Pus Cell Clumps</td><td>Nominal</td><td>present, notpresent</td></tr>
    <tr><td>9</td><td>ba</td><td>Bacteria</td><td>Nominal</td><td>present, notpresent</td></tr>
    <tr><td>10</td><td>bgr</td><td>Blood Glucose Random</td><td>Numerical</td><td>mgs/dl</td></tr>
    <tr><td>11</td><td>bu</td><td>Blood Urea</td><td>Numerical</td><td>mgs/dl</td></tr>
    <tr><td>12</td><td>sc</td><td>Serum Creatinine</td><td>Numerical</td><td>mgs/dl</td></tr>
    <tr><td>13</td><td>sod</td><td>Sodium</td><td>Numerical</td><td>mEq/L</td></tr>
    <tr><td>14</td><td>pot</td><td>Potassium</td><td>Numerical</td><td>mEq/L</td></tr>
    <tr><td>15</td><td>hemo</td><td>Hemo-globin</td><td>Numerical</td><td>gms</td></tr>
    <tr><td>16</td><td>pcv</td><td>Packed Cell Volume</td><td>Numerical</td><td>%</td></tr>
    <tr><td>17</td><td>wc</td><td>White Blood Cell Count</td><td>Numerical</td><td>cells/cumm</td></tr>
    <tr><td>18</td><td>rc</td><td>Red Blood Cell Count</td><td>Numerical</td><td>millions/cmm</td></tr>
    <tr><td>19</td><td>htn</td><td>Hypertension</td><td>Nominal</td><td>yes, no</td></tr>
    <tr><td>20</td><td>dm</td><td>Diabetes Mellitus</td><td>Nominal</td><td>yes, no</td></tr>
    <tr><td>21</td><td>cad</td><td>Coronary Artery Disease</td><td>Nominal</td><td>yes, no</td></tr>
    <tr><td>22</td><td>appet</td><td>Appetite</td><td>Nominal</td><td>good, poor</td></tr>
    <tr><td>23</td><td>pe</td><td>Pedal Edema</td><td>Nominal</td><td>yes, no</td></tr>
    <tr><td>24</td><td>ane</td><td>Anemia</td><td>Nominal</td><td>yes, no</td></tr>
    <tr><td>25</td><td>class</td><td>Class</td><td>Nominal</td><td>ckd, notckd</td></tr>
  </tbody>
</table>

<h2 id="5-data-preprocessing">5. Data Preprocessing</h2>
<ul>
<li>Nominal strings → numerical encoding.  </li>
<li>Four preprocessing strategies:  </li>
<li>Drop columns with many nulls.  </li>
<li>Drop rows with many nulls.  </li>
<li>kNN imputation.  </li>
<li>Forward-fill (ffill).  </li>
</ul>
<p>Scaling:<br>
- <strong>StandardScaler</strong> for ML models.<br>
- <strong>RobustScaler</strong> for CNN.  </p>
<p>Split: 80% training, 20% testing.  </p>
<hr>
<h2 id="6-models-used">6. Models Used</h2>
<ul>
<li><strong>Machine Learning</strong>: Naive Bayes, Logistic Regression, Decision Tree, Random Forest, Support Vector Machine.  </li>
<li><strong>Deep Learning</strong>: CNN Sequential model (3 layers: 8 neurons → 4 neurons (ReLU) → 1 neuron (Sigmoid)).  </li>
</ul>
<hr>
<h2 id="7-performance-metrics">7. Performance Metrics</h2>
<p>Evaluation criteria: <strong>Accuracy, Precision, Recall, F1-Score</strong></p>
<h3 id="table-2-accuracy">Table 2: Accuracy</h3>
<table border="1" cellspacing="0" cellpadding="5">
<tr><th>Dataset</th><th>CNN</th><th>RF</th><th>DT</th><th>NB</th><th>LR</th><th>SVM</th></tr>
<tr><td>D1</td><td>100</td><td>100</td><td>98.75</td><td>95</td><td>100</td><td>98.75</td></tr>
<tr><td>D2</td><td>100</td><td>98.1</td><td>94.3</td><td>96.2</td><td>98.1</td><td>98.1</td></tr>
<tr><td>D3</td><td>100</td><td>100</td><td>97.5</td><td>98.8</td><td>100</td><td>100</td></tr>
<tr><td>D4</td><td>100</td><td>100</td><td>100</td><td>98.8</td><td>100</td><td>100</td></tr>
<tr><td>Average</td><td>100</td><td>99.52</td><td>97.63</td><td>97.2</td><td>99.52</td><td>99.21</td></tr>
</table>

<h3 id="table-3-precision">Table 3: Precision</h3>
<table border="1" cellspacing="0" cellpadding="5">
<tr><th>Dataset</th><th>CNN</th><th>RF</th><th>DT</th><th>NB</th><th>LR</th><th>SVM</th></tr>
<tr><td>D1</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>98.1</td></tr>
<tr><td>D2</td><td>100</td><td>100</td><td>94.4</td><td>90.5</td><td>95</td><td>95</td></tr>
<tr><td>D3</td><td>100</td><td>100</td><td>95.6</td><td>100</td><td>100</td><td>100</td></tr>
<tr><td>D4</td><td>100</td><td>100</td><td>100</td><td>98.1</td><td>100</td><td>100</td></tr>
<tr><td>Average</td><td>100</td><td>100</td><td>97.5</td><td>97.15</td><td>98.75</td><td>98.27</td></tr>
</table>

<h3 id="table-4-recall">Table 4: Recall</h3>
<table border="1" cellspacing="0" cellpadding="5">
<tr><th>Dataset</th><th>CNN</th><th>RF</th><th>DT</th><th>NB</th><th>LR</th><th>SVM</th></tr>
<tr><td>D1</td><td>100</td><td>100</td><td>98.1</td><td>92.3</td><td>100</td><td>100</td></tr>
<tr><td>D2</td><td>100</td><td>95.8</td><td>89.5</td><td>100</td><td>100</td><td>100</td></tr>
<tr><td>D3</td><td>100</td><td>100</td><td>100</td><td>98.1</td><td>100</td><td>100</td></tr>
<tr><td>D4</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr>
<tr><td>Average</td><td>100</td><td>98.95</td><td>96.9</td><td>97.6</td><td>100</td><td>100</td></tr>
</table>

<h3 id="table-5-f1-score">Table 5: F1-Score</h3>
<table border="1" cellspacing="0" cellpadding="5">
<tr><th>Dataset</th><th>CNN</th><th>RF</th><th>DT</th><th>NB</th><th>LR</th><th>SVM</th></tr>
<tr><td>D1</td><td>100</td><td>100</td><td>99</td><td>96</td><td>100</td><td>99</td></tr>
<tr><td>D2</td><td>100</td><td>97.9</td><td>91.9</td><td>95</td><td>97.4</td><td>97.4</td></tr>
<tr><td>D3</td><td>100</td><td>100</td><td>97.7</td><td>99</td><td>100</td><td>100</td></tr>
<tr><td>D4</td><td>100</td><td>100</td><td>100</td><td>99</td><td>100</td><td>100</td></tr>
<tr><td>Average</td><td>100</td><td>99.47</td><td>97.15</td><td>97.25</td><td>99.35</td><td>99.1</td></tr>
</table>

<hr>
<h2 id="8-results-conclusion">8. Results &amp; Conclusion</h2>
<ul>
<li><strong>Best Model</strong>: CNN achieved <strong>100% accuracy, precision, recall, and F1-Score</strong> across all datasets.  </li>
<li><strong>Next Best</strong>: Random Forest and Logistic Regression (avg. accuracy: 99.52%).  </li>
<li><strong>Other Models</strong>: SVM (99.21%), Decision Tree (97.63%), Naive Bayes (97.2%).  </li>
</ul>
<p><strong>Conclusion</strong>: Deep learning with CNN offers the most accurate predictions for CKD, but ensemble models (RF) and simpler models (LR, SVM) also perform very well, providing cost-effective alternatives.</p>
<h2 id="references">References</h2>
<p>[1] Agarwal, S.K. &amp; Srivastava, R.K. (2009). <em>Chronic Kidney Disease in India: Challenges and Solutions.</em> Nephron Clinical Practice, 111, C197–C203.  </p>
<p>[2] Webster, A.C., Nagler, E.V., Morton, R.L., &amp; Masson, P. (2017). <em>Chronic Kidney Disease.</em> Lancet, 389(10075), 1238–1252. doi:10.1016/S0140-6736(16)32064-5.</p>
