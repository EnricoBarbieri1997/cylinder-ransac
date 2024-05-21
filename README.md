# cylinder-ransac
A USAC implementation of ransac for cylinder fitting.

# Main Components
## USAC
The main class in this codebase is USAC in `usac/usac.py`. It defines the steps of the USAC algorithm and provides methods for running the algorithm on a given dataset.

The main USAC class is a combination of the template and delegator OOP design patterns.

The USAC templates define the following steps:

- Pre-processing
- Number of iterations choosing
- Filtering
- Sampling *
- Sample check
- Model generation *
- Model checking
- Verification *
- Degeneracy test
- Evaluation
- Model refinement
- Post processing

Steps marked with an asterix are mandatory for an USAC implementation to be valid while default fake steps that act as missing are provided for all the remaining ones

## USAC builder and factory
USACBuilder is a utility class that let's you configure each step of the USAC algorithm before building the actual object to run it.

USACFactory is a factory patter as the name suggests that provides ready to use implementations of the general USAC for specific cases like:

- Line fitting
- Cylinder fitting
	- As a general quadric
	- From 2 points with normals
	- From 3 points without normals

## Strategies
In each subfolder of the `usac` directory a `strategy.py` file defines the general interface of an algorithm step. The following strategies are available:

- [PreProcessingStrategy](PreProcessingStrategy.md)
- [NumberOfIterationsStrategy](NumberOfIterationsStrategy.md)
- [PrefilteringStrategy](PrefilteringStrategy.md)
- [SamplingStrategy](SamplingStrategy.md)
- [SampleCheckStrategy](SampleCheckStrategy.md)
- [ModelGenerationStrategy](ModelGenerationStrategy.md)
- [ModelCheckStrategy](ModelCheckStrategy.md)
- [VerificationStrategy](VerificationStrategy.md)
- [DegeneracyStrategy](DegeneracyStrategy.md)
- [EvaluationStrategy](EvaluationStrategy.md)
- [ModelRefinementStrategy](ModelRefinementStrategy.md)
- [PostProcessingStrategy](PostProcessingStrategy.md)

# Model generation steps
## Cylinders
### As a quadric surface
9 points are taken and fitted to the quadric surface characteristic equation `A * x**2 + B * y**2 + C * z**2 + D * x * y + E * x * z + F * y * z + G * x + H * y + I * z + 1`
the resulting quadric is not strictly a cylinder.

### From 2 points with normals
A detailed explaination is available [here](https://github.com/CloudCompare/CloudCompare/issues/1237). A summary of the steps is provided:
- Take the vector orthogonal to both point normals using the cross product. This is the cylinder axis
- Build a plane with normal direction equal to the cylinder axis and passing throug an arbitrary point
- Project both points and relative normal directions to said plane
- Intersect the projected points with normals. This is the cylinder center
- Calculate the distance between the center and one of this points. This is the radius

### From 3 points
Using a [circumcircle](https://en.wikipedia.org/wiki/Circumcircle):
- Build a triangle from 3 points
- Find the intersection of two of the said triangle bisectors. This is the center
- Take the normal of the triangle. This is the axis
- Calculate the distance between the center and one of the points. This is the radius
