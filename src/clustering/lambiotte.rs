use crate::graph::{PyGraph};
use crate::dictmap::*;
use petgraph::visit::{IntoEdges, Visitable, IntoNeighbors};
use petgraph::algo::Measure;
use pyo3::prelude::PyResult;
use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use std::collections::HashSet;
use std::fmt;
use reunion::{UnionFind, UnionFindTrait};


#[derive(Debug)]
pub struct Cluster<G>
    where G: IntoEdges + IntoNeighbors + Visitable,
          G::NodeId: Hash
{
    pub level: usize,
    pub total_weight_inside: isize,
    pub total_weight_around: isize,
    pub nodes: Vec<G::NodeId>
}

impl<G> PartialEq for Cluster<G>
where
    G: IntoEdges + IntoNeighbors + Visitable,
    G::NodeId: Hash
{
    fn eq(&self, other: &Self) -> bool {
        (self.level == other.level)
        && (self.total_weight_around == other.total_weight_around)
        && (self.total_weight_inside == other.total_weight_inside)
        && (self.nodes.len() == other.nodes.len())
        && (
            self.nodes.iter().zip(other.nodes.iter()).all(|(&s_node, &o_node)| s_node.eq(&o_node))
        )
    }
}

impl<G> Eq for Cluster<G>
where
    G: IntoEdges + IntoNeighbors + Visitable,
    G::NodeId: Hash
{

}

impl<G> Clone for Cluster<G>
where
    G: IntoEdges + IntoNeighbors + Visitable,
    G::NodeId: Hash
{
    fn clone(&self) -> Self {
        Cluster {
            level: self.level,
            total_weight_around: self.total_weight_around,
            total_weight_inside: self.total_weight_inside,
            nodes: self.nodes.clone()
        }
    }
}

impl<G> Hash for Cluster<G>
where G: IntoEdges + IntoNeighbors + Visitable,
      G::NodeId: Hash
{
    fn hash<H: Hasher>(&self, state: &mut H) {
        state.write_usize(self.level);
        state.write_isize(self.total_weight_inside);
        state.write_isize(self.total_weight_around);
        state.write_usize(self.nodes.len());
        // For now, let's just go with a loose requirement.
        // Maybe we should have NodeId hashable later.
        state.finish();
    }
}

// TODO: We can precompute k_i as well. Think where though.


pub fn cluster<G, F, K>(
    graph: G,
    max_iterations: usize,
    weight_fn: F
) -> Vec<Cluster<G>>
where 
    G: IntoEdges + Visitable + IntoNeighbors,
    F: Fn(G::EdgeRef) -> PyResult<K>,
    K: Measure + Copy,
    G::NodeId: Hash
{
    let uf: UnionFind<Cluster<G>> = UnionFind::new();
    println!("uf");

    println!("{:?}", max_iterations);
    vec![]
}
