/*
 * queue.h
 *
 * Created: 11/4/2016 11:30:10 AM
 *  Author: antda685
 */ 


#ifndef QUEUE_H_
#define QUEUE_H_

#include <stddef.h>
#include <stdbool.h>

struct queue
{
	struct queue* next;
	void* data;
};

struct queue* queue_create();
void queue_free(struct queue* q);
void* queue_front(struct queue* q);
void queue_pop(struct queue* q);
void queue_push(struct queue* q, void* data);
bool queue_empty(struct queue* q);

#endif /* QUEUE_H_ */