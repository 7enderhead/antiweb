/* 
@start(__macros__)
@define(__codeprefix__)

The code begins in file @subst(__file__) at line @subst(__line__):
@enifed(__codeprefix__)

@end(__macros__)

@start()
_ant_send_message
=================

.. function:: int _ant_send_message(asm_t* self, uchar_t msg_id, uchar_t channel,\
                                    const uchar_t data[], uchar_t data_size, ant_msg_t *response)
   
   Sends a message to the ANT chip 

   :param msg_id: The id of the ANT message to be send.
   :param channel: The channel number.
   :param data: The data to be send.
   :param data_size: the size of the data
   :param response: If the caller wants the message's response, it can set \
                    this argument to a :ref:`ant_msg_t` buffer, it can     \
                    can be also set to ``NULL``.
   @code */

int _ant_send_message(asm_t* self, uchar_t msg_id, uchar_t channel, 
		      const uchar_t data[], uchar_t data_size, 
		      ant_msg_t* response) {
  uchar_t msgbuffer[sizeof(ant_msg_t) + 1];    /* message + sync byte */
  ant_msg_t *msg = (ant_msg_t*)(msgbuffer+1);
  uchar_t chksum, *p;
  size_t msg_size = (sizeof(msg->id)
		     +sizeof(msg->size)
		     +sizeof(msg->channel)
		     +data_size);
  int i, error, retry=0;

  if (_keyboard_interrupted())
    return MR_ABORTED;

  if (ant_is_recovering(self))
    return MR_RECOVERING;

  /*@cstart(build message)*/
  msgbuffer[0] = MESG_TX_SYNC;
  msg->size = data_size+1; /* +1 for channel */
  msg->id = msg_id;
  msg->channel = channel;
  memcpy(msg->data, data, data_size);
  
  chksum = 0;
  for (i = 0, p = msgbuffer; i < (int)msg_size+1; i++, p++)
    chksum ^= *p;
  
  msg->data[data_size++] = chksum; 
  msg->data[data_size++] = 0;
  msg->data[data_size] = 0;

  #if _DEBUG_LEVEL >= 1
  print_log("#_ant_send_message: %s(%i) ", 
	    get_message_name(msg->id), 
	    (int)msg->channel);
  print_message_bytes(msg);
  print_log("-%u\n", (ushort_t)(ant_clock() & 0xFFFF));
  #endif

  if (ant_is_waiting_for_response(self))
    CHECK(MR_WRONG_STATE);

  /*@(build message)*/

_try_again:

  CHECK(_ant_write(self, msgbuffer, msg_size+4)); 
     /* 4 == +sizeof(sync)+sizeof(checksum)+2*sizeof(0) */
  
  error = _ant_wait_for_response(self, msg, response, 0);

  /*@cstart(time out handling)*/
  if (error == MR_TIMEOUT 
      && retry < 10
      && msg_id != MESG_ACKNOWLEDGED_DATA_ID
      && msg_id != MESG_BURST_DATA_ID) {
    char zeros[15];

    retry++;
    memset(zeros, 0, sizeof(zeros));
    _ant_write(self, zeros, sizeof(zeros));
    goto _try_again;
  }
  /*@(time out handling)*/

  CHECK(error);

  BEGIN_EXCEPT;
  print_exception();
  END_EXCEPT;

  return error;
}

/* @edoc
   @rinclude(build message)

   .. _time out handling:

   **<<time out handling>>**

   If we got a timeout, ANT probably didn't get the message. According to 
   `"ant message protocol and usage" <http://www.thisisant.com/images/Resources/PDF/1204662412_ant%20message%20protocol%20and%20usage.pdf>`_  section 9.5.2, we send some 0 bytes and try again.

   @include(time out handling)

   @*/
