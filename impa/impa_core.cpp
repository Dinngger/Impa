#include <sstream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>

namespace py = pybind11;

enum ColorType: int8_t {
    RED,
    YELLOW,
    BLUE
};

enum NodeType: int8_t {
    SIMPLE,
    BIG,
    BLINKER,
    WALKMAN
};

struct Pos {
    int8_t x;
    int8_t y;
    Pos(int8_t x, int8_t y) : x(x), y(y) {}
    bool operator==(const Pos& p) const {
        return x == p.x && y == p.y;
    }
    bool operator!=(const Pos& p) const {
        return !(*this == p);
    }
    Pos operator+(const Pos& p) const {
        return Pos(x + p.x, y + p.y);
    }
};

std::array<Pos, 4> relative_neighbors = {
    Pos(0, 1), Pos(1, 0), Pos(0, -1), Pos(-1, 0)};

struct Node {
    bool valid = false;
    NodeType type = SIMPLE;
    int8_t size = 0;
    ColorType color = YELLOW;
    ColorType next_color = YELLOW;
    Pos another_pos = Pos(0, 0);
    std::vector<Pos> neighbors() const {
        std::vector<Pos> result;
        if (type == BIG) {
            for (const auto& delta : relative_neighbors) {
                Pos neighbor = delta;
                Pos other_neighbor = another_pos + delta;
                if (neighbor != another_pos)
                    result.emplace_back(neighbor);
                if (other_neighbor != Pos(0, 0))
                    result.emplace_back(other_neighbor);
            }
        } else {
            for (const auto& delta : relative_neighbors) {
                result.emplace_back(delta);
            }
        }
        return result;
    }
};

class Map {
    int8_t h=0, w=0;
    std::vector<Node> nodes;
    std::vector<size_t> dynamic_nodes;
    Node& get(Pos p) {return nodes[p.x + p.y * w];}
public:
    bool success() const {
        for (const auto& node : nodes) {
            if (node.valid && node.size != node.color)
                return false;
        }
        return true;
    }
    void click(Pos p) {
        Node& n = get(p);
        if (!n.valid || n.size == 0)
            return;
        n.size--;
        for (const Pos& neighbor_pos : n.neighbors()) {
            Node& neighbor = this->get(p + neighbor_pos);
            if (neighbor.valid && neighbor.size < 2)
                neighbor.size++;
        }
        for (size_t i : dynamic_nodes) {
            Node& dn = nodes[i];
            switch (dn.type) {
            case SIMPLE: break;
            case BIG: break;
            case BLINKER:
                std::swap(dn.color, dn.next_color);
                break;
            case WALKMAN:
                dn.valid = !dn.valid;
                break;
            }
        }
    }
    void load(std::string t) {
        int state = 0;
        int row_cnt = 0, col_cnt = 0;
        ColorType color, next_color;
        t = t + "\n";
        for (char c : t) {
            switch (state) {
            case 0:
                switch (c) {
                case ' ': break;
                case 'R': color = RED; state = 1; break;
                case 'Y': color = YELLOW; state = 1; break;
                case 'B': color = BLUE; state = 1; break;
                case 'x': nodes.emplace_back(); col_cnt++; break;
                case '\n':
                    if (col_cnt == 0) break;
                    if (w == 0)
                        w = col_cnt;
                    else {
                        if (w != col_cnt)
                            throw std::runtime_error("Column width mismatch.");
                    }
                    col_cnt = 0;
                    row_cnt++;
                    break;
                default:
                    std::stringstream ss;
                    ss << "Unexpected char '" << c << "'.";
                    throw std::runtime_error(ss.str());
                }
                break;
            case 1:
                switch (c) {
                case ' ': break;
                case 'R': next_color = RED; state = 2; break;
                case 'Y': next_color = YELLOW; state = 2; break;
                case 'B': next_color = BLUE; state = 2; break;
                case '0':
                case '1':
                case '2': {
                    Node new_node{true, SIMPLE, int8_t(c - '0'), color,};
                    nodes.emplace_back(new_node);
                    col_cnt++;
                    state = 0;
                    break;
                }
                default:
                    std::stringstream ss;
                    ss << "Unexpected char '" << c << "'.";
                    throw std::runtime_error(ss.str());
                }
                break;
            case 2:
                switch (c) {
                case ' ': break;
                case '0':
                case '1':
                case '2': {
                    Node new_node{true, BLINKER, int8_t(c - '0'), color, next_color};
                    nodes.emplace_back(new_node);
                    dynamic_nodes.push_back(nodes.size() - 1);
                    col_cnt++;
                    state = 0;
                    break;
                }
                default:
                    std::stringstream ss;
                    ss << "Unexpected char '" << c << "'.";
                    throw std::runtime_error(ss.str());
                }
                break;
            }
        }
        h = row_cnt;
    }
};

PYBIND11_MODULE(impa_core, m) {
    m.doc() = "impa_core";
    py::class_<Map>(m, "Map")
        .def(py::init())
        .def("success", &Map::success)
        .def("click", [](Map& self, int x, int y) {self.click(Pos(x, y));})
        .def("load", &Map::load);
}
