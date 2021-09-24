use crate::graph;
// use crate::graph::NodeId;
use petgraph::visit::{EdgeRef, IntoEdges, VisitMap, Visitable};
use crate::dictmap::*;
use crate::graph::PyGraph;
use petgraph::prelude::*;
use pyo3::prelude::*;
use pyo3::Python;
use pyo3::types::{PyDict};
use super::weight_callable;

pub mod lambiotte;

/// Docstring containing description of the function
#[pyfunction(max_levels = "10")]
#[pyo3(
    text_signature = "(graph, /, max_levels=10)"
)]
pub fn cluster_lambiotte(
    py: Python,
    graph: &PyGraph,
    max_levels: Option<usize>,
    weight_fn: Option<PyObject>,

) -> PyResult<PyObject> {
    /* Your code goes here */
    let result = lambiotte::cluster(
        graph,
        max_levels.unwrap_or(0),
        |e| weight_callable(py, &weight_fn, e.weight(), 0_f64)
    );
    // lambiotte::cluster();
    let mut output = PyDict::new(py);
    println!("{:?}", &output);
    // output.items()
    

    Ok(PyDict::new(py).into())
}

#[cfg(test)]
mod tests {
    // IntoNeighbors + Visitable
    use crate::lambiotte::*;
    use crate::graph::PyGraph;
    use petgraph::visit::{IntoEdgeReferences, Data, GraphBase, GraphRef, IntoNeighbors};
}
