# reyscoring


The Rey–Osterrieth Complex Figure (ROCF) Test, developed by Rey in 1941 and standardized by Osterrieth in 1944, serves as a prominent neuropsychological evaluation tool for assessing visuospatial constructional ability and visual memory. The ROCF consists of a complex drawing featuring 39 straight-line segments and circular components with three solid dots shown as below. 

![The-18-scoring-units-of-the-Rey-Osterrieth-Complex-Figure](https://github.com/EmmaHLU/reyscoring/assets/124171401/b6e590ab-3683-42fc-9bce-22a97215f3dd)

Traditionally, scoring this intricate figure has been a meticulous and error-prone task conducted by professionals due to its complexity.

Addressing the challenge posed by the data-intensive nature of deep learning models and the difficulty in obtaining sufficient hand-drawn ROCF data, I devised a simulation program based on computer vision. This program generates synthetic hand-drawn ROCF figures along with their corresponding scores. Subsequently, this synthetic dataset was utilized to train a DenseNet model. To enhance the model's performance, fine-tuning was performed using a more limited real dataset (figures drawn by humans).

As a result, the project achieved impressive metrics on the testing set, boasting a Mean Absolute Error (MAE) of 1.24 and an R-squared value of 0.97. The model is currently undergoing continuous training to further optimize its performance and refine its predictive capabilities.
