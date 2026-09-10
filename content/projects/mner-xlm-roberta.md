---
Title: Multilingual NER — Corpus Sampling for Indian Languages
Slug: mner-xlm-roberta
Project Type: University Project
Duration: May 2022 - Jul 2022
Summary: Fine-tuned XLM-RoBERTa for multilingual Named Entity Recognition (NER) on Indian languages.
Skills: Large Language Models (LLM) · Transformer Models · Named Entity Recognition (NER) · NLP · Python
Image: mner-xlm-roberta.jpg
Order: 5
---

<h2 id="overview">Overview</h2>
<p>Fine-tuned XLM-RoBERTa for multilingual Named Entity Recognition (NER) on Indian languages.  </p>
<h2 id="highlights">Highlights</h2>
<ul>
<li>Sampled Hindi, Bengali, Marathi, Telugu, Tamil, and Malayalam corpora from PAN-X according to spoken proportions.  </li>
<li>Achieved effective multilingual NER performance across multiple Indian languages.  </li>
</ul>
<h2 id="repository">Repository</h2>
<p><a href="https://github.com/shrishtinigam/multilingual_named_entity_recognition">multilingual_named_entity_recognition - GitHub Link</a></p>
<h1 id="multilingual-ner-corpus-sampling-for-indian-languages">Multilingual NER — Corpus Sampling for Indian Languages</h1>
<p>This project fine-tunes <strong>XLM-RoBERTa</strong> for <strong>multilingual Named Entity Recognition (NER)</strong> across Indian languages using the PAN-X dataset. </p>
<p>The goal is to build a representative Indian corpus and evaluate cross-lingual transfer performance.</p>
<h2 id="dataset">Dataset</h2>
<ul>
<li><strong>Base dataset:</strong> <a href="https://huggingface.co/datasets/xtreme">PAN-X (WikiAnn subset from XTREME benchmark)</a></li>
<li><strong>Languages considered:</strong> Hindi, Bengali, Marathi, Telugu, Tamil, Malayalam  </li>
<li><strong>Sampling strategy:</strong> proportional to Indian mother-tongue usage  </li>
</ul>
<h3 id="corpus-construction-representative-sampling">Corpus construction (representative sampling):</h3>
<p>We sample datasets for Hindi, Bengali, Marathi, Telugu, Tamil, and Malayalam from PAN-X in proportions that reflect their spoken (mother-tongue) shares. The original mother-tongue fractions and their normalized percentages (so the six languages sum to 100%) are shown below.</p>
<blockquote>
<p><em>Note:</em> normalized percentages are computed by dividing each language's mother-tongue fraction by the sum of the six fractions (73.8) and scaling to 100. Minor rounding differences (±0.01) may appear.</p>
</blockquote>
<h3 id="language-sampling-proportions">Language sampling proportions</h3>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>Language</th>
      <th>Mother-tongue fraction (%)</th>
      <th>Normalized (out of these 6 → %)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Hindi</td>
      <td style="text-align:right;">43.63</td>
      <td style="text-align:right;">59.12 (≈59.11)</td>
    </tr>
    <tr>
      <td>Bengali</td>
      <td style="text-align:right;">8.03</td>
      <td style="text-align:right;">10.88</td>
    </tr>
    <tr>
      <td>Marathi</td>
      <td style="text-align:right;">6.86</td>
      <td style="text-align:right;">9.30</td>
    </tr>
    <tr>
      <td>Telugu</td>
      <td style="text-align:right;">6.70</td>
      <td style="text-align:right;">9.08</td>
    </tr>
    <tr>
      <td>Tamil</td>
      <td style="text-align:right;">5.70</td>
      <td style="text-align:right;">7.72 (≈7.73)</td>
    </tr>
    <tr>
      <td>Malayalam</td>
      <td style="text-align:right;">2.88</td>
      <td style="text-align:right;">3.90</td>
    </tr>
    <tr>
      <td><b>Total</b></td>
      <td style="text-align:right;"><b>73.80</b></td>
      <td style="text-align:right;"><b>100.00</b></td>
    </tr>
  </tbody>
</table>

<h2 id="methodology">Methodology</h2>
<ol>
<li><strong>Corpus preparation</strong></li>
<li>Sampled PAN-X monolingual corpora proportionally.</li>
<li>Shuffled datasets to avoid bias.</li>
<li>
<p>Aligned tokens with IOB2 NER labels.</p>
</li>
<li>
<p><strong>Modeling</strong></p>
</li>
<li>Base: <strong>XLM-RoBERTa</strong></li>
<li>Custom <strong>token classification head</strong>:<ul>
<li>Dropout + Linear layer</li>
</ul>
</li>
<li>
<p>Loss: <strong>CrossEntropyLoss</strong></p>
</li>
<li>
<p><strong>Training setup</strong></p>
</li>
<li>Fine-tuned for <strong>3 epochs</strong>  </li>
<li>Batch size: <strong>24</strong></li>
<li>
<p>Evaluation: <strong>F1-score</strong> via <code>seqeval</code></p>
</li>
<li>
<p><strong>Evaluation</strong></p>
</li>
<li>Monolingual fine-tuning on Hindi.  </li>
<li>Zero-shot transfer tested on Tamil, Marathi, Bengali.  </li>
<li>Error analysis using per-token loss and confusion matrices.</li>
</ol>
<h2 id="results">Results</h2>
<ul>
<li><strong>Training time:</strong> ~1 hour  </li>
<li><strong>Evaluation metric:</strong> F1-score  </li>
</ul>
<h1 id="xlm-roberta-multilingual-ner-results">XLM-RoBERTa Multilingual NER — Results</h1>
<h2 id="training-configuration">Training Configuration</h2>
<ul>
<li><strong>Dataset size (train):</strong> 2955 examples</li>
<li><strong>Epochs:</strong> 3</li>
<li><strong>Batch size:</strong> 24</li>
<li><strong>Total optimization steps:</strong> 372</li>
<li><strong>Training runtime:</strong> ~1 hour</li>
<li><strong>Final training loss:</strong> 0.3985</li>
</ul>
<h3 id="epoch-wise-performance">Epoch-wise Performance</h3>
<table border="1" cellspacing="0" cellpadding="5"> <tr> <th>Epoch</th> <th>Training Loss</th> <th>Validation Loss</th> <th>F1 Score</th> </tr> <tr> <td>1</td> <td>0.7027</td> <td>0.3816</td> <td>0.7749</td> </tr> <tr> <td>2</td> <td>0.2944</td> <td>0.3326</td> <td>0.8014</td> </tr> <tr> <td>3</td> <td>0.2065</td> <td>0.2894</td> <td>0.8183</td> </tr> </table>

<h2 id="hindi-test-set-591-samples">Hindi (Test Set — 591 samples)</h2>
<table border="1" cellspacing="0" cellpadding="5"><tr> <th>Class</th> <th>Precision</th> <th>Recall</th> <th>F1</th> <th>Support</th> </tr> <tr> <td>LOC</td> <td>0.7572</td> <td>0.7541</td> <td>0.7556</td> <td>244</td> </tr> <tr> <td>ORG</td> <td>0.7817</td> <td>0.8174</td> <td>0.7991</td> <td>219</td> </tr> <tr> <td>PER</td> <td>0.8792</td> <td>0.9066</td> <td>0.8927</td> <td>257</td> </tr> </table>

<p><strong>Overall:</strong><br>
- Micro F1 = <strong>0.8181</strong><br>
- Macro F1 = 0.8158<br>
- Weighted F1 = 0.8178<br>
- Loss = 0.261  </p>
<h2 id="bengali-test-set-93-samples">Bengali (Test Set — 93 samples)</h2>
<table border="1" cellspacing="0" cellpadding="5"><tr> <th>Class</th> <th>Precision</th> <th>Recall</th> <th>F1</th> <th>Support</th> </tr> <tr> <td>LOC</td> <td>0.6667</td> <td>0.6000</td> <td>0.6316</td> <td>30</td> </tr> <tr> <td>ORG</td> <td>0.4667</td> <td>0.6364</td> <td>0.5385</td> <td>22</td> </tr> <tr> <td>PER</td> <td>0.7857</td> <td>0.8049</td> <td>0.7952</td> <td>41</td> </tr> </table>

<p><strong>Overall:</strong><br>
- Micro F1 = <strong>0.6771</strong><br>
- Macro F1 = 0.6551<br>
- Weighted F1 = 0.6817<br>
- Loss = 0.356  </p>
<h2 id="marathi-test-set-109-samples">Marathi (Test Set — 109 samples)</h2>
<table border="1" cellspacing="0" cellpadding="5"><tr> <th>Class</th> <th>Precision</th> <th>Recall</th> <th>F1</th> <th>Support</th> </tr> <tr> <td>LOC</td> <td>0.7708</td> <td>0.8222</td> <td>0.7957</td> <td>45</td> </tr> <tr> <td>ORG</td> <td>0.6111</td> <td>0.7097</td> <td>0.6567</td> <td>31</td> </tr> <tr> <td>PER</td> <td>0.9091</td> <td>0.9091</td> <td>0.9091</td> <td>33</td> </tr> </table>

<p><strong>Overall:</strong><br>
- Micro F1 = <strong>0.7876</strong><br>
- Macro F1 = 0.7872<br>
- Weighted F1 = 0.7905<br>
- Loss = 0.304  </p>
<h2 id="tamil-test-set-116-samples">Tamil (Test Set — 116 samples)</h2>
<table border="1" cellspacing="0" cellpadding="5"> <tr> <th>Class</th> <th>Precision</th> <th>Recall</th> <th>F1</th> <th>Support</th> </tr> <tr> <td>LOC</td> <td>0.7838</td> <td>0.6042</td> <td>0.6824</td> <td>48</td> </tr> <tr> <td>ORG</td> <td>0.6038</td> <td>0.7805</td> <td>0.6809</td> <td>41</td> </tr> <tr> <td>PER</td> <td>0.5556</td> <td>0.7407</td> <td>0.6349</td> <td>27</td> </tr> </table>

<p><strong>Overall:</strong><br>
- Micro F1 = <strong>0.6694</strong><br>
- Macro F1 = 0.6660<br>
- Weighted F1 = 0.6708<br>
- Loss = 0.747  </p>
<h2 id="confusion-matrix-hindi-example">Confusion Matrix (Hindi Example)</h2>
<p><img alt="Confusion Matrix" src="a68e19b5-0bbf-44e1-834a-d3c25a23cbb3.png"></p>
<h2 id="key-observations">Key Observations</h2>
<ul>
<li><strong>Hindi (training language):</strong> Highest F1 (0.818).  </li>
<li><strong>Cross-lingual transfer:</strong>  </li>
<li>Marathi shows strong transfer (F1 ≈ 0.79).  </li>
<li>Bengali and Tamil have weaker transfer (F1 ≈ 0.67).  </li>
<li><strong>Entity-wise trend:</strong>  </li>
<li>PER consistently achieves the best recall and F1 across languages.  </li>
<li>ORG is hardest to detect, especially in Bengali and Tamil.  </li>
</ul>
<h2 id="key-takeaways">Key Takeaways</h2>
<ul>
<li>XLM-RoBERTa is effective for <strong>multilingual NER</strong> in Indian languages.  </li>
<li><strong>Fine-tuning on one high-resource language (Hindi)</strong> transfers reasonably well to others.  </li>
<li><strong>Language similarity</strong> influences transfer quality (closer languages → better zero-shot F1).  </li>
</ul>
<h2 id="future-work">Future Work</h2>
<ul>
<li>Extend to more Indian languages.  </li>
<li>Explore multilingual joint training (instead of single-language fine-tuning).  </li>
<li>Investigate domain adaptation beyond Wikipedia-based corpora.</li>
</ul>
