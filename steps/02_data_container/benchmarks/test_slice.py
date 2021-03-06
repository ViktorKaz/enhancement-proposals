#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["Markus Löning"]
__all__ = []

import numpy as np
from sktime.utils._testing.series_as_features import \
    make_classification_problem

from benchmarks.utils import ak_3d_arr
from benchmarks.utils import ak_record_arr
from benchmarks.utils import np_3d_arr


def _slice(X):
    return X[10:20, 5:15, 50:60]


def _nested_slice(X):
    x = X.iloc[10:20, 5:15]
    return np.asarray([[x.iloc[i, j].iloc[50:60].to_numpy()
                        for j in range(x.shape[1])]
                       for i in range(x.shape[0])])


X, _ = make_classification_problem(n_instances=100,
                                   n_timepoints=100,
                                   n_columns=20)

expected = _slice(np_3d_arr(X))


def test_ak_3d_slice(benchmark):
    x = ak_3d_arr(X)
    actual = benchmark(_slice, x)
    np.testing.assert_array_equal(actual, expected)


def test_ak_record_slice(benchmark):
    x = ak_record_arr(X)
    actual = benchmark(_slice, x)
    np.testing.assert_array_equal(actual["value"], expected)


def test_np_slice(benchmark):
    x = np_3d_arr(X)
    actual = benchmark(_slice, x)
    np.testing.assert_array_equal(actual, expected)


def test_nested_slice(benchmark):
    actual = benchmark(_nested_slice, X)
    np.testing.assert_array_equal(actual, expected)
