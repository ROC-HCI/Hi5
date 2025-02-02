# Setup Guide for Hi5 Unity Project

This guide will outline the steps required to reproduce the Hi5 Data Synthesis Pipeline using the Unity Engine. This guide assumes intermediate knowledge of the Unity Engine.

- Project Link: https://www.dropbox.com/scl/fo/cs5bdynig2a8jazpomul7/AFJ_f9mKHxlsrR60eGn0SRU?rlkey=tw1y19spyxtsca94pz6on2z1j&st=uduvogbm&dl=0

## Requirements:

- Unity Game Engine (version 2021.3.6f1) is installed.
- Hi5 Unity project files are downloaded.
- The Leap Motion Realistic Hands packs have been purchased on the Unity Asset Store
    - Female: https://assetstore.unity.com/packages/3d/characters/humanoids/leap-motion-realistic-female-hands-211090
    - Male: https://assetstore.unity.com/packages/3d/characters/humanoids/leap-motion-realistic-male-hands-109961

## Steps

1. Open the project in Unity
2. Import the Hands from the Asset Store
3. Add the hand prefabs to the scene as children of the `Hands` empty at the same point and hide them
4. Ensure `Assets/main/materials/{male|female}_textures/` are populated with textures for each hand asset for each skin tone
5. Ensure that `Assets/Resources/materials_male/` is populated with materials for each skin tone
6. Since the female hand asset requires two materials, ensure that `Assets/Resources/materials_female/` is populated with sub-folders named for each of their skin tones, and where each sub-folder contains two materials named such that the arm material comes before the hand material.
7. Ensure that the `PlayAllRandom` script attached to the `player` object is populated with the hand assets by updating the Hands array in the script parameters with the hand assets added in step 3. Update the `OUTPUT_PATH` and `CSV_PATH` to a location on your machine.
8. Press Run to begin data synthesis

