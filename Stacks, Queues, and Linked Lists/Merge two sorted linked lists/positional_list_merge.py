# Extend the PositionalList class provided in the Public Files of this Doubly Linked list 
# section of this problem statement with a new public method called merge.
from easyinput import read

class _DoublyLinkedBase:
	"""A base class providing a doubly linked list representation."""

	#-------------------------- nested _Node class --------------------------
	# nested _Node class
	class _Node:
		"""Lightweight, nonpublic class for storing a doubly linked node."""
		__slots__ = '_element', '_prev', '_next'						# streamline memory

		def __init__(self, element, prev, next):						# initialize node's fields
			self._element = element													 # user's element
			self._prev = prev																 # previous node reference
			self._next = next																 # next node reference

	#-------------------------- list constructor --------------------------

	def __init__(self):
		"""Create an empty list."""
		self._header = self._Node(None, None, None)
		self._trailer = self._Node(None, None, None)
		self._header._next = self._trailer									# trailer is after header
		self._trailer._prev = self._header									# header is before trailer
		self._size = 0																			# number of elements

	#-------------------------- public accessors --------------------------

	def __len__(self):
		"""Return the number of elements in the list."""
		return self._size

	def is_empty(self):
		"""Return True if list is empty."""
		return self._size == 0

	#-------------------------- nonpublic utilities --------------------------

	def _insert_between(self, e, predecessor, successor):
		"""Add element e between two existing nodes and return new node."""
		newest = self._Node(e, predecessor, successor)			# linked to neighbors
		predecessor._next = newest
		successor._prev = newest
		self._size += 1
		return newest

	def _delete_node(self, node):
		"""Delete nonsentinel node from the list and return its element."""
		predecessor = node._prev
		successor = node._next
		predecessor._next = successor
		successor._prev = predecessor
		self._size -= 1
		element = node._element														 # record deleted element
		node._prev = node._next = node._element = None			# deprecate node
		return element																			# return deleted element

	
class PositionalList(_DoublyLinkedBase):
	"""A sequential container of elements allowing positional access."""

	#-------------------------- nested Position class --------------------------
	class Position:
		"""An abstraction representing the location of a single element.

		Note that two position instances may represent the same inherent
		location in the list.	Therefore, users should always rely on
		syntax 'p == q' rather than 'p is q' when testing equivalence of
		positions.
		"""

		def __init__(self, container, node):
			"""Constructor should not be invoked by user."""
			self._container = container
			self._node = node
		
		def element(self):
			"""Return the element stored at this Position."""
			return self._node._element
			
		def __eq__(self, other):
			"""Return True if other is a Position representing the same location."""
			return type(other) is type(self) and other._node is self._node

		def __ne__(self, other):
			"""Return True if other does not represent the same location."""
			return not (self == other)							 # opposite of __eq__
		
	#------------------------------- utility methods -------------------------------
	def _validate(self, p):
		"""Return position's node, or raise appropriate error if invalid."""
		if not isinstance(p, self.Position):
			raise TypeError('p must be proper Position type')
		if p._container is not self:
			raise ValueError('p does not belong to this container')
		if p._node._next is None:									# convention for deprecated nodes
			raise ValueError('p is no longer valid')
		return p._node

	def _make_position(self, node):
		"""Return Position instance for given node (or None if sentinel)."""
		if node is self._header or node is self._trailer:
			return None															# boundary violation
		else:
			return self.Position(self, node)				 # legitimate position
		
	#------------------------------- accessors -------------------------------
	def first(self):
		"""Return the first Position in the list (or None if list is empty)."""
		return self._make_position(self._header._next)

	def last(self):
		"""Return the last Position in the list (or None if list is empty)."""
		return self._make_position(self._trailer._prev)

	def before(self, p):
		"""Return the Position just before Position p (or None if p is first)."""
		node = self._validate(p)
		return self._make_position(node._prev)

	def after(self, p):
		"""Return the Position just after Position p (or None if p is last)."""
		node = self._validate(p)
		return self._make_position(node._next)

	def __iter__(self):
		"""Generate a forward iteration of the elements of the list."""
		cursor = self.first()
		while cursor is not None:
			yield cursor.element()
			cursor = self.after(cursor)

	#------------------------------- mutators -------------------------------
	# override inherited version to return Position, rather than Node
	def _insert_between(self, e, predecessor, successor):
		"""Add element between existing nodes and return new Position."""
		node = super()._insert_between(e, predecessor, successor)
		return self._make_position(node)

	def add_first(self, e):
		"""Insert element e at the front of the list and return new Position."""
		return self._insert_between(e, self._header, self._header._next)

	def add_last(self, e):
		"""Insert element e at the back of the list and return new Position."""
		return self._insert_between(e, self._trailer._prev, self._trailer)

	def add_before(self, p, e):
		"""Insert element e into list before Position p and return new Position."""
		original = self._validate(p)
		return self._insert_between(e, original._prev, original)

	def add_after(self, p, e):
		"""Insert element e into list after Position p and return new Position."""
		original = self._validate(p)
		return self._insert_between(e, original, original._next)

	def delete(self, p):
		"""Remove and return the element at Position p."""
		original = self._validate(p)
		return self._delete_node(original)	# inherited method returns element

	def replace(self, p, e):
		"""Replace the element at Position p with e.

		Return the element formerly at Position p.
		"""
		original = self._validate(p)
		old_value = original._element			 # temporarily store old element
		original._element = e							 # replace with new element
		return old_value										# return the old element value


	#------------------------------- merge -------------------------------

	def merge(self, other):
		"""
		Pre: self and other are two lists sorted in ascending order.
		Post: After the merge operation 'self' contains its previous
					elements and all the elements in 'other' is ascending
					order. Furhtermore, 'other' is empty.
		Observation: Because 'other' must be empty after carring out
			 the merge operation, there is no need to create new nodes.
		"""
		# Vull anar ficant self en ordre
		i = self.first()		# identifico primeres posicions
		j = other.first()
		while j is not None:		
			if i is not None:
				if j.element() < i.element(): 					# ara ja miro elements dintre de posicions
					self.add_before(i, other.delete(j))			# el return de delete és el mateix que borro
					j = other.first()							# he borrat un de j per tant el primer de j és un altre
				else:
					i = self.after(i)							# si i.element < j.element, llavors aques element ja està ben ficat, passo al altre
			else:												# self list no té elements, però j si
				self.add_last(other.delete(j))
				j = other.first()


if __name__ == '__main__':
	n = read(int)
	t1 = PositionalList()
	for i in range(n):
		t1.add_last(read(float))			# no longer int, but floats
	n = read(int)
	t2 = PositionalList()
	for i in range(n):
		t2.add_last(read(float))
	t1.merge(t2)
	print('t1', end='')
	for e in t1:
		print(' ',e,end='')		  # acaba amb un canvi de linia a acda element, cosa que no vull
	print('\nt2', end='')
#	for e in t2:              # per construcció estarà buit
#		print(' ',e)
