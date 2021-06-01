/*
 * Animagrad (AMG)
 * (c) Andriy Babak 2019
 * 
 * date: 10/01/2019
 * modified: 28/05/2021 17:19:15
 * 
 * Author: Andriy Babak
 * e-mail: ababak@gmail.com
 * ------------------------------
 * description: Python module for Maya polygon checking
 * ------------------------------
 * Call from Maya Python:
 *      import cpp
 *      cpp.call("*", lib="maya_module", func="ls")
 *
 *      # Result: ['|front',
 *      '|front|frontShape',
 *      '|pCube1',
 *      '|pCube1|pCubeShape1',
 *      '|pSphere1',
 *      '|pSphere1|pSphereShape1',
 *      '|persp',
 *      '|persp|perspShape',
 *      '|side',
 *      '|side|sideShape',
 *      '|top',
 *      '|top|topShape'] # 
 */

#include <boost/format.hpp>
#include <boost/python.hpp>

#include <maya/MGlobal.h>
#include <maya/MObject.h>
#include <maya/MStatus.h>
#include <maya/MString.h>
#include <maya/MDagPath.h>
#include <maya/MSelectionList.h>

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

API py::object ls(const py::tuple &args, const py::dict &kw)
{
    //
    // Get a list of Maya objects
    //
    string node;
    string full_path;
    MSelectionList sel;
    MDagPath m_dag_path;
    py::list result;
    if (py::len(args) == 1)
        node = py::extract<string>(args[0]);
    else
        node = "*";
    if (sel.add(MString(node.c_str())) != MS::kSuccess)
        return raise_attribute_error((boost::format("Node \"%s\" not found") % node).str());
    for (int i = 0, l = sel.length(); i < l; i++)
    {
        if (sel.getDagPath(i, m_dag_path) != MS::kSuccess)
            continue;
        full_path = m_dag_path.fullPathName().asUTF8();
        result.append(full_path);
    }
    return result;
}
