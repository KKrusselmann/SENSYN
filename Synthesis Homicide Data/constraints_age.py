import pandas as pd
import numpy as np

# custom constraint such that if age is under 18, type is kindermoord
# NOTE: all rows in original data must adhere to the constraint

# age is 1, type is 2


# this function checks validity of data; does it follow the constraint?
def is_valid(column_names, data, extra_parameter):
    col1, col2 = column_names[0], column_names[1]
    cat1, cat2 = extra_parameter["cat1"], extra_parameter["cat2"]
    # data is invalid if type is kindermoord and age is not in age cat
    validity = ~((data[col2].isin(cat2)) & (~data[col1].isin(cat1)))
    return pd.Series(validity)


# this function transforms input data such that constrained columns do not obfuscate other relationships in the data
# whenever age is under 18 and type is not kindermoord, we will replace age with a likely category (most occuring)
# this will allow the synthetic data model to learn the 'type' distribution without 'kindermoord' category, as this only occurs when age is under 18
# note that this is similar to a simple imputation strategy, and more sophisticated imputation strategies are also possible
def transform(column_names, data, extra_parameter):
    col1, col2 = column_names[0], column_names[1]
    cat1, cat2 = extra_parameter["cat1"], extra_parameter["cat2"]

    # whenever type is kindermoord replace age with category NOT IN child ages
    # category is randomly sampled from the proportions OUTSIDE of child ages

    # get total props
    age_props = data[col1][data[col2].isin(cat2)].value_counts(normalize=True)
    # drop child age props
    age_props = age_props.drop(cat1)
    # normalize so sums to 1
    age_props /= age_props.sum()
    # take samples
    sample = np.random.choice(
        age_props.index, p=age_props.values, size=(data[col2].isin(cat2)).sum()
    )
    # fill in sample
    data[col1] = data[col1].mask(data[col2].isin(cat2), sample)

    return data


# this function transforms data sampled from the synthetic data model such that it follows the constraint
# this function is the import one; it should force the synthetic data to always adhere to the constraint
# however, note that this function should be the reverse transformation of the transform function above
# this reverse transformation is simple; whenever age is under 18, replace the type with kindermoord
def reverse_transform(column_names, data, extra_parameter):
    col1, col2 = column_names[0], column_names[1]
    cat1, cat2 = extra_parameter["cat1"], extra_parameter["cat2"]
    # whenever type is kindermoord, set age to one of the correct categories

    # find proportion of age categories for when type is kindermoord (in real data)
    age_props = data[col1][data[col2].isin(cat2)].value_counts(normalize=True)

    # Sample from the categories according to their proportions
    sample = np.random.choice(
        age_props.index, p=age_props.values, size=(data[col2].isin(cat2)).sum()
    )

    # fill the age category with randomly sampled ages whenever type is kindermoord
    data[col1] = data[col1].mask(data[col2].isin(cat2), sample)

    return data


# now we create the custom constraint as a class to later add it to our synthetic data model
from sdv.constraints import create_custom_constraint_class

kindermoordConstraintClass = create_custom_constraint_class(
    is_valid_fn=is_valid, transform_fn=transform, reverse_transform_fn=reverse_transform
)

# all of the above has to be in a separate python file (.py)
# --------------------------------------------------------------------------------------------------------------
