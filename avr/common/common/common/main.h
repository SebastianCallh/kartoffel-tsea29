/*
 * main.h
 *
 * Created: 11/7/2016 11:41:03 AM
 *  Author: antda685
 */ 


#ifndef MAIN_H_
#define MAIN_H_

typedef void(*loopHandler)();

int run_program(loopHandler handler);

#endif /* MAIN_H_ */