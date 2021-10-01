# Video Fuzzer Design

1. Intended audience
- Everyone directly/indirectly involved with video analytics.
- Requirement classification:
    - Research: Experimentation, how changing a feature brings variance to performance (think of a base vid and changing 1 feature/vid)
    - Executor: Would want a (minimal) set of videos that brings out max variation in performance.

2. Can't foresee all use cases. Should provide good enough set of features, but also allow extensibility.

3. Properties to fuzz:
- dimension, bitrate, fps, o/p format, num vids to generate, distribution and kind of objects, transformations, transitions, crop, to overlap or not, obj sizes, ...

4. Provide defaults so user can get started quickly.

5. Executor might just want a bunch of videos with certain objects+distribution. A static config file to provide configutation should be enough.
- python videofuzzer -f config.json

6. An advanced user might want custom transforms, transitions, etc. Allow easy modification and generation.
- python custom_fuzzer.py [-f config.json] (where custom fuzzer extendes transformers etc)

7. Transformer:
- given a video clip, provides basic set of transform classses.
- for custom tranforms, user extends Transformer, that allow directly modifying clip object.
- moviepy allows fade in/out blur, b/w, other fx functions. Allow directly calling them as a lambda?

8. TransitionPoint: 
- we were changing videos every 2s. but that is limiting.
- directly accessing fps/time can also be confusing.
- transition point to abstract that detail out and user only needs to specify what is required in this point

9. Transition:
- allow access to history of all transitionpoints. user might have 5 vids and change 1 at a time.
- allow all new frames or modification of existing frames.
- eg swap videos around 1/1
- uuid as identifier

10. Composition:
- How to fill main frame with multiple videos
- might want a certain design
- specify algo to fill frame or custom design
- would need some info about what is where and of what size

11. Fuzzer
- main controller that reads config and decides how videos need to be generated
- use appropriate compositor, transition, transformer to generate bunch of videos

12. How does it all tie up?
- Fuzzer has all props. From the distributions, it get the set of videos to use. 
- it now sends the videos to transition that will decide what happens to each video next.
- transition one by one sends the videos to transform that decides how each video needs to be transformed. 
- this set of clips is now sent to compositor to decide how to place the videos in the frame
- the video should be ready for a transition point.
- start over
- state needs to be maintained
- fuzzer now based on requirements, can spawn out multiple video generation based on experimenter/executor/other

13. Config
- mostly json
- heirarchical with inheritance
- specify props which are used as default
- can specify multiple sets of videos below with specific individual props
- eg
```
{
    ..
    fps: 25,
    allow_overlap: false,
    transformers: [
        {
            type: skew
            some_prop: 10
        }
    ]
    fuzzer: {
        type: experiment,
        transformers: [
            {
                type: b/w, ..
            },
            {
                type: rotate,
                angle: 45
            }
        ]
    }
    object_class: [car, person, motorbike],
    distribution: {
        type: normal,
        mean: 1,
        variance, 1
    }
    ..
}
```
fps, overlap, distribution, obj_class etc are global. a fuzzer is created which is of type experiment. This will create 3 vids- baseline, one with b/w and one with rotate 45deg. 
- this allows global and local props.
- fuzzer could also be an array allowing multiple sets of videos to be generated.

13. Result
- Provide video, distribution of obj+type, bbox of object


