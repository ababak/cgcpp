/*
 * (c) Andriy Babak 2019-2024
 * 
 * date: 23/01/2019
 * modified: 30/05/2024 10:41:16
 * 
 * Author: Andriy Babak
 * e-mail: ababak@gmail.com
 * ------------------------------
 * description: Exception tesr
 * ------------------------------
 */

#include <boost/python.hpp>

using namespace std;
namespace py = boost::python;

#define API extern "C" BOOST_SYMBOL_EXPORT

API py::object call(const py::tuple &args, const py::dict &kw)
{
    // Throw AttributeError("Some Error") exception
    PyErr_SetString(PyExc_AttributeError, "Some error");
    py::throw_error_already_set();
    return py::object();
}
