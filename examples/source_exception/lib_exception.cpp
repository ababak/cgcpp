/*
 * Animagrad (AMG)
 * 
 * date: 23/01/2019
 * modified: 25/05/2021 19:18:42
 * 
 * Author: Viktor Lavrentev
 * e-mail: viktor.lavrentev@animagrad.com
 * ------------------------------
 * description: Dynamic Library Loader
 * ------------------------------
 */

#include <boost/python.hpp>

using namespace std;
namespace py = boost::python;

#define API extern "C" BOOST_SYMBOL_EXPORT

API py::object call(const py::tuple &args, const py::dict &kw)
{
    PyErr_SetString(PyExc_AttributeError, "Some error");
    py::throw_error_already_set();
    return py::object();
}
