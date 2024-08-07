/*
 * (c) Andriy Babak 2022-2024
 *
 * date: 05/08/2022
 * modified: 30/05/2024 10:40:58
 *
 * Author: Andriy Babak
 * e-mail: ababak@gmail.com
 * ------------------------------
 * description: Sample Houdini module
 * ------------------------------
 * Call from Houdini Python:
 *      >>> import cgcpp
 *      >>> cgcpp.call("/", lib="d:/cgcpp/out/houdini_module", func="ls")
 *      ['/obj', '/out', '/ch', '/shop', '/img', '/img/comp1', '/vex', '/mat', '/stage', '/tasks', '/tasks/topnet1', '/tasks/topnet1/localscheduler']
*/
 

#include <iostream>
#include <boost/format.hpp>
#include <boost/python.hpp>

#include <OP/OP_Director.h>
#include <SOP/SOP_Node.h>
#include <UT/UT_String.h>
#include <UT/UT_NTStreamUtil.h>

#define API extern "C" BOOST_SYMBOL_EXPORT

using namespace std;
namespace py = boost::python;

py::object raise_attribute_error(const string &error_message)
{
    PyErr_SetString(
        PyExc_AttributeError,
        error_message.c_str());
    py::throw_error_already_set();
    return py::object();
}

void traverse(OP_Network *parent, py::list &result)
{
    OP_Node *node;
    for (int i = 0, nkids = parent->getNchildren(); i < nkids; i++)
    {
        node = parent->getChild(i);
        UT_String path_string;
        node->getFullPath(path_string);
        string full_path = path_string.toStdString();
        result.append(full_path);
        cout << full_path << "\n";
        if (node->isNetwork())
        {
            traverse((OP_Network *)node, result);
        }
    }
}

API py::object ls(const py::tuple &args, const py::dict &kw)
{
    //
    // Get a list of Houdini objects
    //
    string path;
    OP_Network *parent;
    py::list result;
    if (py::len(args) == 1)
        path = py::extract<string>(args[0]);
    else
        path = "/obj";
    parent = (OP_Network *)OPgetDirector()->findNode(path.c_str());
    if (!parent)
        return raise_attribute_error((boost::format("Node \"%s\" not found") % path).str());
    cout << "Traversing " << path << "\n";
    traverse(parent, result);
    return result;
}
