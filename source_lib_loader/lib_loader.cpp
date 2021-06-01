/*
 * (c) Andriy Babak 2021
 * 
 * date: 07/09/2020
 * modified: 31/05/2021 18:48:45
 * 
 * Author: Andriy Babak
 * e-mail: ababak@gmail.com
 * ------------------------------
 * description: Dynamic Library Loader
 * ------------------------------
 */

#include <string>
#include <boost/dll.hpp>
#include <boost/python.hpp>
#include <boost/filesystem.hpp>

const std::string __version__ = "1.0.2";

namespace py = boost::python;
using lib_function_t = py::object(const py::tuple &, const py::dict &);

// Usage example:
// >>> lib_loader.call(2, 3, lib="power.dll", func="pow")
py::object call(const py::tuple &args, const py::dict &kwargs)
{
    boost::filesystem::path lib_path = (std::string)py::extract<std::string>(kwargs["lib"]);
    std::string function_name = py::extract<std::string>(kwargs["func"]);
    std::function<lib_function_t> lib_function;
    lib_function = boost::dll::import<lib_function_t>(lib_path, function_name);
    try
    {
        return lib_function(args, kwargs);
    }
    catch (...)
    {
        py::handle_exception();
        py::throw_error_already_set();
        return py::object();
    }
}

BOOST_PYTHON_MODULE(lib_loader)
{
    py::scope().attr("__version__") = __version__;
    py::def("call", py::raw_function(call));
}
