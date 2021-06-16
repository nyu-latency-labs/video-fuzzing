#include <gst/gst.h>
#include <stdio.h>

/* Structure to contain all our information, so we can pass it to callbacks */
typedef struct _VideoCompositor {
  GstElement *pipeline;
  GstElement *background;
  GstElement *decode;
  GstElement *imagefreeze;
  GstElement *compositor;
  GstElement *convert;
  GstElement *sink;
  int overlayCount;
} VideoCompositor;

typedef struct _OverlayVideo {
  GstElement *source;
  GstElement *decode;
  GstElement *convert;
  VideoCompositor *compositor;
  int overlayCount;
} OverlayVideo;

/* Handler for the pad-added signal */
static void pad_added_handler (GstElement *src, GstPad *pad, VideoCompositor *data);
static void video_pad_added_handler (GstElement *src, GstPad *new_pad, OverlayVideo *data);
static int add_overlay_video (char videoUri[], VideoCompositor compositor);

int main(int argc, char *argv[]) {
  GstBus *bus;
  GstMessage *msg;
  GstStateChangeReturn ret;
  gboolean terminate = FALSE;

  VideoCompositor videoCompositor;
  videoCompositor.overlayCount = 0;

  /* Initialize GStreamer */
  gst_init (&argc, &argv);

  /* Compositor init */
  videoCompositor.background = gst_element_factory_make ("filesrc", "background");
  videoCompositor.decode = gst_element_factory_make ("decodebin", "decode");
  videoCompositor.imagefreeze = gst_element_factory_make ("imagefreeze", "imagefreeze");
  videoCompositor.compositor = gst_element_factory_make("compositor", "compositor");
  videoCompositor.convert = gst_element_factory_make("videoconvert", "videoconvert");
  videoCompositor.sink = gst_element_factory_make("filesink", "finalsink");

  videoCompositor.pipeline = gst_pipeline_new ("compositor_pipeline");

  if (!videoCompositor.pipeline || !videoCompositor.background || !videoCompositor.decode || !videoCompositor.imagefreeze 
      || !videoCompositor.compositor || !videoCompositor.convert || !videoCompositor.sink) {
    g_printerr ("Not all elements could be created.\n");
    return -1;
  }

  gst_bin_add_many (GST_BIN (videoCompositor.pipeline), videoCompositor.background, videoCompositor.decode, videoCompositor.imagefreeze,
                             videoCompositor.compositor, videoCompositor.convert, videoCompositor.sink, NULL);
  
  if (!gst_element_link_many (videoCompositor.background, videoCompositor.decode, NULL)) {
    g_printerr ("Elements could not be linked.\n");
    gst_object_unref (videoCompositor.pipeline);
    return -1;
  }

  // if (!gst_element_link_many (videoCompositor.imagefreeze, videoCompositor.compositor, videoCompositor.convert, videoCompositor.sink, NULL)) {
  if (!gst_element_link_many (videoCompositor.compositor, videoCompositor.convert, videoCompositor.sink, NULL)) {
    g_printerr ("Elements could not be linked.\n");
    gst_object_unref (videoCompositor.pipeline);
    return -1;
  }

  // g_object_set (videoCompositor.background, "location", "./resources/street.jpg", NULL);
  g_object_set (videoCompositor.background, "location", "./resources/cars/1.mp4", NULL);
  g_object_set (videoCompositor.sink, "location", "./file", NULL);

  /* Connect to the pad-added signal */
  g_signal_connect (videoCompositor.decode, "pad-added", G_CALLBACK (pad_added_handler), &videoCompositor);
  add_overlay_video("./resources/cars/1.mp4", videoCompositor);

  ret = gst_element_set_state (videoCompositor.pipeline, GST_STATE_PLAYING);
  if (ret == GST_STATE_CHANGE_FAILURE) {
    g_printerr ("Unable to set the pipeline to the playing state.\n");
    gst_object_unref (videoCompositor.pipeline);
    return -1;
  }
  

  /* Listen to the bus */
  bus = gst_element_get_bus (videoCompositor.pipeline);
  do {
    msg = gst_bus_timed_pop_filtered (bus, GST_CLOCK_TIME_NONE,
        GST_MESSAGE_STATE_CHANGED | GST_MESSAGE_ERROR | GST_MESSAGE_EOS);

    /* Parse message */
    if (msg != NULL) {
      GError *err;
      gchar *debug_info;

      switch (GST_MESSAGE_TYPE (msg)) {
        case GST_MESSAGE_ERROR:
          gst_message_parse_error (msg, &err, &debug_info);
          g_printerr ("Error received from element %s: %s\n", GST_OBJECT_NAME (msg->src), err->message);
          g_printerr ("Debugging information: %s\n", debug_info ? debug_info : "none");
          g_clear_error (&err);
          g_free (debug_info);
          terminate = TRUE;
          break;
        case GST_MESSAGE_EOS:
          g_print ("End-Of-Stream reached.\n");
          terminate = TRUE;
          break;
        case GST_MESSAGE_STATE_CHANGED:
          /* We are only interested in state-changed messages from the pipeline */
          if (GST_MESSAGE_SRC (msg) == GST_OBJECT (videoCompositor.pipeline)) {
            GstState old_state, new_state, pending_state;
            gst_message_parse_state_changed (msg, &old_state, &new_state, &pending_state);
            g_print ("Pipeline state changed from %s to %s:\n",
                gst_element_state_get_name (old_state), gst_element_state_get_name (new_state));
          }
          break;
        default:
          /* We should not reach here */
          g_printerr ("Unexpected message received.\n");
          break;
      }
      gst_message_unref (msg);
    }
  } while (!terminate);

  /* Free resources */
  gst_object_unref (bus);
  gst_element_set_state (videoCompositor.pipeline, GST_STATE_NULL);
  gst_object_unref (videoCompositor.pipeline);
  return 0;
}

/* This function will be called by the pad-added signal */
static void pad_added_handler (GstElement *src, GstPad *new_pad, VideoCompositor *data) {
  GstPad *sink_pad = gst_element_get_request_pad (data->compositor, "sink");
  GstPadLinkReturn ret;
  GstCaps *new_pad_caps = NULL;
  GstStructure *new_pad_struct = NULL;
  const gchar *new_pad_type = NULL;

  g_print ("Received new pad '%s' from '%s':\n", GST_PAD_NAME (new_pad), GST_ELEMENT_NAME (src));

  /* If our converter is already linked, we have nothing to do here */
  if (gst_pad_is_linked (sink_pad)) {
    g_print ("We are already linked. Ignoring.\n");
    goto exit;
  }

  /* Check the new pad's type */
  new_pad_caps = gst_pad_get_current_caps (new_pad);
  new_pad_struct = gst_caps_get_structure (new_pad_caps, 0);
  new_pad_type = gst_structure_get_name (new_pad_struct);
  if (!g_str_has_prefix (new_pad_type, "video/x-raw")) {
    g_print ("It has type '%s' which is not raw video. Ignoring.\n", new_pad_type);
    goto exit;
  }

  /* Attempt the link */
  ret = gst_pad_link (new_pad, sink_pad);
  if (GST_PAD_LINK_FAILED (ret)) {
    g_print ("Type is '%s' but link failed.\n", new_pad_type);
  } else {
    g_print ("Link succeeded (type '%s').\n", new_pad_type);
  }

exit:
  /* Unreference the new pad's caps, if we got them */
  if (new_pad_caps != NULL)
    gst_caps_unref (new_pad_caps);

  /* Unreference the sink pad */
  gst_object_unref (sink_pad);
}

static int add_overlay_video (char videoUri[], VideoCompositor compositor) {
  GstStateChangeReturn ret;
  OverlayVideo *video = (OverlayVideo*) malloc (sizeof(OverlayVideo));
  video->compositor =  &compositor;
  
  compositor.overlayCount = 1 + compositor.overlayCount;
  char bgName[20];
  sprintf(bgName, "background%d", compositor.overlayCount);
  char decodeName[20];
  sprintf(decodeName, "decode%d", compositor.overlayCount);
  char convertName[20];
  sprintf(convertName, "videoconvert%d", compositor.overlayCount);

  video->source = gst_element_factory_make ("filesrc", bgName);
  video->decode = gst_element_factory_make ("decodebin", decodeName);
  video->convert = gst_element_factory_make("videoconvert", convertName);
  video->overlayCount = compositor.overlayCount;

  if (!video->source || !video->decode || !video->convert) {
    g_printerr ("Not all elements could be created.\n");
    return -1;
  }

  gst_bin_add_many (GST_BIN (compositor.pipeline), video->source, video->decode, video->convert, NULL);
  
  if (!gst_element_link_many (video->source, video->decode, NULL)) {
    g_printerr ("Elements could not be linked.\n");
    gst_object_unref (compositor.pipeline);
    return -1;
  }
  
  if (!gst_element_link_many (video->convert, compositor.compositor, NULL)) {
    g_printerr ("Elements could not be linked.\n");
    gst_object_unref (compositor.pipeline);
    return -1;
  }

  /*
  // In info logs, I got no sink for compositor, so I try to manually link sink and src which fails.
  GstPad *compositorSinkPad = gst_element_get_request_pad(compositor.compositor, "sink_%u");
  GstPad *videoconvertSrcPad = gst_element_get_static_pad(video->convert, "src");
  if (!gst_pad_link(videoconvertSrcPad, compositorSinkPad)) {
    g_printerr ("Elements could not be linked src sink.\n");
    gst_object_unref (compositor.pipeline);
    return -1;
  }
  */

  g_object_set (video->source, "location", videoUri, NULL);

  /* Connect to the pad-added signal */
  g_signal_connect (video->decode, "pad-added", G_CALLBACK (video_pad_added_handler), video);

  ret = gst_element_set_state (compositor.pipeline, GST_STATE_PLAYING);
  if (ret == GST_STATE_CHANGE_FAILURE) {
    g_printerr ("Unable to set the pipeline to the playing state.\n");
    gst_object_unref (compositor.pipeline);
    return -1;
  }
  return 0;
}

/* This function will be called by the pad-added signal */
static void video_pad_added_handler (GstElement *src, GstPad *new_pad, OverlayVideo *data) {
  gboolean done = FALSE;
  GstPad *sink_pad = gst_element_get_static_pad (data->convert, "sink");

  GstPadLinkReturn ret;
  GstCaps *new_pad_caps = NULL;
  GstStructure *new_pad_struct = NULL;
  const gchar *new_pad_type = NULL;

  g_print ("Received new pad '%s' from '%s':\n", GST_PAD_NAME (new_pad), GST_ELEMENT_NAME (src));

  /* If our converter is already linked, we have nothing to do here */
  if (gst_pad_is_linked (sink_pad)) {
    g_print ("We are already linked. Ignoring.\n");
    goto exit;
  }

  /* Check the new pad's type */
  new_pad_caps = gst_pad_get_current_caps (new_pad);
  new_pad_struct = gst_caps_get_structure (new_pad_caps, 0);
  new_pad_type = gst_structure_get_name (new_pad_struct);
  if (!g_str_has_prefix (new_pad_type, "video/x-raw")) {
    g_print ("It has type '%s' which is not raw video. Ignoring.\n", new_pad_type);
    goto exit;
  }
  
  /* Attempt the link */
  ret = gst_pad_link (new_pad, sink_pad);
  if (GST_PAD_LINK_FAILED (ret)) {
    g_print ("Type is '%s' but link failed.\n", new_pad_type);
  } else {
    g_print ("Link succeeded (type '%s').\n", new_pad_type);
  }

exit:
  /* Unreference the new pad's caps, if we got them */
  if (new_pad_caps != NULL)
    gst_caps_unref (new_pad_caps);

  /* Unreference the sink pad */
  gst_object_unref (sink_pad);
}