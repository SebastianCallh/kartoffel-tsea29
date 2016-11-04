/*
 * queue.c
 *
 * Created: 11/4/2016 11:30:03 AM
 *  Author: antda685
 */ 

#include "queue.h"

struct queue queue_create() {
	struct queue q* = new struct queue;
	q->next = NULL;
	q->data = NULL;
	
	return q;
}

void queue_free(struct queue q*) {
	struct queue current* = q;
	while (current != NULL) {
		struct queue next* = current->next;
		free(current->data);
		free(current);
		current = next;
	}
}

void* queue_front(struct queue q*) {
	assert(q->data == NULL);
	
	struct queue* front = q->next;
	if (front != NULL) {
		return front->data;
	} else {
		return NULL;	
	}
}

void queue_pop(struct queue q*) {
	assert(q->data == NULL);
	assert(!queue_empty(q));
	
	struct queue old* = q->next;	
	q->next = q->next->next;
	
	if (old != NULL) {
		old->next = NULL;
		queue_free(old);
	}
}

void queue_push(struct queue q*, void* data) {
	assert(q->data == NULL);
	
	struct queue* tail = &q;
	while (tail->next != NULL) {
		tail = tail->next;
	}
	
	struct queue next = queue_create();
	next->data = data;
	
	tail->next = &next;
}

bool queue_empty(struct queue q*) {
	assert(q->data == NULL);
	
	return q->next == NULL;
}
