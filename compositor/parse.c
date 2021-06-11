

#include <stdio.h>
#include <string.h>
#include <gst/gst.h>
#include <glib.h>

gboolean callback(gpointer data)
{
    GstElement *pipeline = (GstElement *)data;
    GstElement *imagefreeze = gst_bin_get_by_name(GST_BIN(pipeline), "imagefreeze");
    // send eos but doesnt work for some reason
    gst_element_send_event (pipeline, gst_event_new_eos ()); 

    // another version that works
    GstBus* bus = gst_pipeline_get_bus(GST_PIPELINE(pipeline));
    gst_bus_post(bus, gst_message_new_eos(GST_OBJECT(imagefreeze)));
    gst_object_unref(bus);
    // // custom message is recieved
    // GstMessage *msg = gst_message_new_custom(GST_MESSAGE_ELEMENT, GST_OBJECT(pipeline), NULL);
    // gst_element_post_message(GST_ELEMENT(pipeline), msg);
    return FALSE;
}

gboolean
bus_call(GstBus *bus, GstMessage *msg, gpointer data)
{
    gchar *debug = NULL;
    GError *err = NULL;

    switch (GST_MESSAGE_TYPE(msg))
    {
    case GST_MESSAGE_EOS:
        g_printerr("eos");
        g_main_loop_quit ((GMainLoop *) data);
        break;

    case GST_MESSAGE_ERROR:
        gst_message_parse_error(msg, &err, &debug);
        g_printerr("Error: %s\n", err->message);

        g_main_loop_quit((GMainLoop *)data);

        if (err)
        {
            g_error_free(err);
        }

        if (debug)
        {
            g_free(debug);
        }

        break;
    case GST_MESSAGE_STATE_CHANGED:
        break;
    case GST_MESSAGE_ELEMENT:
        g_main_loop_quit((GMainLoop *)data);
        break;
    default:
        g_printerr("Unexpected message type detected! %d %s\n", GST_MESSAGE_TYPE(msg),gst_message_type_get_name(GST_MESSAGE_TYPE(msg)));
        break;
    }

    return TRUE;
}

int main(int argc, char *argv[])
{
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);
    gst_init(&argc, &argv); // init gstreamer

    GError *err = NULL;
    GstBus *bus;
    GstMessage *msg;
    GstStateChangeReturn ret;
    gboolean terminate = FALSE;

    // GstElement* pipeline = gst_parse_launch("filesrc location=\"./resources/street.jpg\" ! decodebin ! imagefreeze num-buffers=200 ! videoconvert ! compositor name=composite ! x264enc ! mp4mux ! filesink location=./file.mp4 filesrc location=\"./resources/cars/1.mp4\" ! video/x-raw, width=100, height=100! decodebin ! videoconvert ! composite.", &err);
    // GstElement *pipeline = gst_parse_launch("filesrc location=./resources/street.jpg ! decodebin ! imagefreeze name=\"imagefreeze\" ! videoconvert  ! x264enc ! h264parse ! mp4mux reserved-moov-update-period=100000 ! filesink location=./file.mp4", &err);
    GstElement *pipeline = gst_parse_launch("filesrc location=./resources/cars/1.mp4 name=\"imagefreeze\" ! decodebin ! videoconvert  ! x264enc ! h264parse ! mp4mux reserved-moov-update-period=100000 ! filesink location=./file.mp4", &err);
    // gst-launch-1.0 filesrc location=./resources/cars/1.mp4 ! decodebin ! videoconvert ! x264enc ! mp4mux ! filesink location=./gg.mp4
    // gst-launch-1.0 filesrc location=./resources/street.jpg ! decodebin ! imagefreeze num-buffers=100 ! videoconvert  ! x264enc ! mp4mux reserved-moov-update-period=100000000 ! filesink location=./ggg.mp4    

    bus = gst_element_get_bus(pipeline);
    gst_bus_add_watch(bus, bus_call, loop);
    gst_object_unref(bus);
    
    // g_timeout_add_seconds(15, callback, pipeline);
    
    gst_element_set_state(pipeline, GST_STATE_PLAYING);
    g_print("run loop\n");
    g_main_loop_run(loop);
    gst_element_set_state(pipeline, GST_STATE_NULL);
    g_print("end loop\n");

    /* Free resources */
    gst_object_unref(pipeline);
    return 0;
}
