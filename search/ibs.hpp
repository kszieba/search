// Copyright © 2020 the Search Authors under the MIT license. See AUTHORS for the list of authors.                                                             
#pragma once                                                                    
#include "../search/search.hpp"                                                 
#include "../utils/pool.hpp"
                                                                                
template <class D> struct BeamSearch : public SearchAlgorithm<D> {

	typedef typename D::State State;
	typedef typename D::PackedState PackedState;                                
	typedef typename D::Cost Cost;                                              
	typedef typename D::Oper Oper;

	struct Node {
		int openind; //open index is an integer, unsurprisingly
		Node *parent; //parent is a pointer to a Node
		PackedState state; //state will be a PackedState
		Oper op, pop;  //op and pop are operators?
		Cost f, g;

		/*constructor for node struct*/
		Node() : openind(-1) {  //place initially at end?
		}

		static ClosedEntry<Node, D> &closedentry(Node *n) { //what is this?
			return n->closedent;
		}

		static PackedState &key(Node *n) { //again, feed in reference to a node
			return n->state;
		}

		/* Set index of node on open list. */
		static void setind(Node *n, int i) {
			n->openind = i;
		}

		/* Get index of node on open list. */
		static int getind(const Node *n) {
			return n->openind;
		}

		/* Indicates whether Node a has better value than Node b. */
		static bool pred(Node *a, Node *b) {
			if (a->f == b->f) //if f-values are the same
				return a->g > b->g; //return whether a's g-value is greater than b's
			return a->f < b->f; //otherwise return a's f-value is greater than b's
		}

		/* Priority of node. */
		static Cost prio(Node *n) { //returns f-value
			return n->f;
		}

		/* Priority for tie breaking. */
		static Cost tieprio(Node *n) { //returns g-value
			return n->g;
		}

    private:
		ClosedEntry<Node, D> closedent;
    
	};

	BeamSearch(int argc, const char *argv[]) :
		SearchAlgorithm<D>(argc, argv), closed(30000001) { //what is closed here?
		dropdups = false;
		for (int i = 0; i < argc; i++) {
			if (i < argc - 1 && strcmp(argv[i], "-width") == 0)
				width = atoi(argv[++i]);
			if (strcmp(argv[i], "-dropdups") == 0)
				dropdups = true; //drop duplicates is false if not specified
		}

		if (width < 1)
			fatal("Must specify a >0 beam width using -width");
    
		nodes = new Pool<Node>();
	}

	~BeamSearch() {
		delete nodes;
	}

	void search(D &d, typename D::State &s0) {
		this->start();
		closed.init(d);  //initializes closed list for the domain?

		Node *n0 = init(d, s0); //takes domain and start state and initializes node
		//closed.add(n0);
		open.push(n0);  //open and closed both declared at bottom

		int depth = 0; // can set variable to something at same time it's declared


		bool done = false; //declares a boolean done and assigns false (to be changed later)
    
		while (!open.empty() && !done && !SearchAlgorithm<D>::limit()) {
			depth++; //gradually increases depth, as IBS does
      
			Node **beam = new Node*[width];
			int c = 0; //begin at index 0
			while(c < width && !open.empty()) {  //while there is still room within beam width 
			// and open not empty
				Node *n = open.pop();

				unsigned long hash = n->state.hash(&d); /* use hash function belonging to state of
				node pointed to by n and give it the address of d 
				for state struct in domain, hash function is necessary*/
				Node *dup = closed.find(n->state, hash); //give n's state and created hash to
				// find function
				if(!dup) { //if no duplicate found
				  closed.add(n, hash);
				} else {
				  SearchAlgorithm<D>::res.dups++;
				  if(!dropdups && n->g < dup->g) { //if not dropping duplicates and node n's 
				  // g is greater than dup's g
					SearchAlgorithm<D>::res.reopnd++;
					
					dup->f = dup->f - dup->g + n->g; //change f of dup to reflect n's g rather 
					//than dup's (avoids recalculating heuristic)
					dup->g = n->g; 
					dup->parent = n->parent;
					dup->op = n->op;
					dup->pop = n->pop;
					//overall, replace dup with n by changing member variables
				  } else {
					continue;
				  }
				}

				beam[c] = n; //sets index c of beam array to end
				c++; //adds one to c (will eventually end loop, if open list is not exhausted)
			}

			if(c == 0) { //used to keep later actions from being carried out
			//is triggered if width is 0 or open was empty
			  done = true;
			}

			while(!open.empty())
			  open.pop();
			//open.clear();   //commented out, for some reason?
      
			for(int i = 0; i < c && !done && !SearchAlgorithm<D>::limit(); i++) {
				Node *n = beam[i];
				State buf, &state = d.unpack(buf, n->state); //what is buf?

				expand(d, n, state);
			}

			if(cand) {
			  solpath<D, Node>(d, cand, this->res); /*solpath exists within search.hpp  
			  Would 'this' refer
              to the template, or something closer?*/
			  done = true;
			}

			delete[] beam; //empties beam of pointers to nodes
		}
		this->finish();  //according to search.hpp, finish must be called to stop collecting
		//information
	}

	virtual void reset() {  //why is virtual used here
		SearchAlgorithm<D>::reset();
		open.clear();
		closed.clear();
		delete nodes;
		nodes = new Pool<Node>();
	}

	virtual void output(FILE *out) {  //where does file come from?
		SearchAlgorithm<D>::output(out);
		closed.prstats(stdout, "closed ");  //Where is prstats? (Answer: closedlist.hpp)
		dfpair(stdout, "open list type", "%s", open.kind());
		dfpair(stdout, "node size", "%u", sizeof(Node));
	}


private:

	void expand(D &d, Node *n, State &state) { //a reference to d, which is of type D?
		SearchAlgorithm<D>::res.expd++;  //adds one to result's expanded node count

		typename D::Operators ops(d, state);
		for (unsigned int i = 0; i < ops.size(); i++) {
			if (ops[i] == n->pop)
				continue;
			SearchAlgorithm<D>::res.gend++;
			considerkid(d, n, state, ops[i]);
		}
	}

	void considerkid(D &d, Node *parent, State &state, Oper op) {
		Node *kid = nodes->construct();
		assert (kid);
		typename D::Edge e(d, state, op);
		kid->g = parent->g + e.cost;
		d.pack(kid->state, e.state);

		kid->f = kid->g + d.h(e.state);
		kid->parent = parent;
		kid->op = op;
		kid->pop = e.revop;
		
		State buf, &kstate = d.unpack(buf, kid->state);
		if (d.isgoal(kstate) && (!cand || kid->g < cand->g)) { /*if is solution and either candidate
		does not exist or kid has a lower g (g for solution is equivalent to f)*/
		  cand = kid;
		}
		
		open.push(kid);  //is this logical when kid is a solution?
	}

	Node *init(D &d, State &s0) {
		Node *n0 = nodes->construct();
		d.pack(n0->state, s0);
		n0->g = Cost(0);
		n0->f = d.h(s0);
		n0->pop = n0->op = D::Nop;
		n0->parent = NULL;
		cand = NULL;
		return n0;
	}

    int width;
    bool dropdups;
	OpenList<Node, Node, Cost> open;
 	ClosedList<Node, Node, D> closed;
	Pool<Node> *nodes;
	Node *cand;
  
};
