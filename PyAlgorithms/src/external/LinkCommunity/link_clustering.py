#!/usr/bin/env python
# encoding: utf-8

from optparse import OptionParser
from ..LinkCommunity.graph_io_helper import *
from ..LinkCommunity.link_clustering_algo import *


class MyParser(OptionParser):
    def format_epilog(self, formatter):
        return self.epilog


def detect_communities(threshold, is_weighted, dendro_flag, output_dir, basename):
    if is_weighted:
        adj, edges, ij2wij = read_edge_list_weighted(basename)
    else:
        adj, edges = read_edge_list_unweighted(basename)

    # print(edges)
    if threshold is not None:
        if is_weighted:
            edge2cid, D_thr = HLC(adj, edges).single_linkage(threshold, w=ij2wij)
        else:
            edge2cid, D_thr = HLC(adj, edges).single_linkage(threshold)
        # print("# D_thr = %f" % D_thr)
        write_edge2cid(edge2cid, output_dir)
    else:
        if is_weighted:
            edge2cid, S_max, D_max, list_D = HLC(adj, edges).single_linkage(w=ij2wij)
        else:
            if dendro_flag:
                edge2cid, S_max, D_max, list_D, orig_cid2edge, linkage = HLC(adj, edges).single_linkage(
                    dendro_flag=dendro_flag)
                write_dendro("%s_dendro" % basename, orig_cid2edge, linkage)
            else:
                edge2cid, S_max, D_max, list_D = HLC(adj, edges).single_linkage()

        # f = open("%s_thr_D.txt" % basename, 'w')
        # for s, D in list_D:
        #     print >> f, s, D
        # f.close()
        # print("# D_max = %f\n# S_max = %f" % (D_max, S_max))
        write_edge2cid(edge2cid, output_dir)


if __name__ == '__main__':
    usage = "usage: python %prog [options] filename"
    parser = MyParser(usage)
    parser.add_option("-t", "--threshold", dest="threshold", type="float", default=None,
                      help="threshold to cut the dendrogram (optional)")
    parser.add_option("-w", "--weighted", dest="is_weighted", action="store_true", default=False,
                      help="is the network weighted?")
    parser.add_option("-r", "--record-dendrogram", dest="dendro_flag", action="store_true",
                      default=False, help="recording the whole dendrogram (optional)")
    parser.add_option("-o", "--output-dir", dest="output", type="str", default=".",
                      help="output directory")
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    threshold = options.threshold
    is_weighted = options.is_weighted
    dendro_flag = options.dendro_flag
    output_dir = options.output

    print("# loading network from edgelist...")
    basename = os.path.splitext(args[0])[0]

    detect_communities(threshold, is_weighted, dendro_flag, output_dir, basename)
