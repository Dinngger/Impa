#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>

namespace py = pybind11;

enum NodeType {
    Simple,
};

class Node {
};

class Impa {
public:
    Map m;
    Map m_init;
    Impa(Map init): m_init(init) {
        reset();
    }
    void reset() {
        m = m_init;
    }
};

PYBIND11_MODULE(impa, m) {
    m.doc() = "impa";
    py::class_<Impa>(m, "Impa")
        .def(py::init<int>())
        .def_readwrite("op_type", &Device::op_type)
        .def_readwrite("pos", &Device::pos)
        .def("__contains__", [](Device* device, int time){return device->contains(time);})
        .def_readwrite("times", &Device::times);
}
