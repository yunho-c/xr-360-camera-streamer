import enum
from typing import Dict, Optional

class BoneId(enum.IntEnum):
    """
    A Python enumeration that corresponds to the C# OVRSkeleton.BoneId enum,
    used in VR/AR development for skeletal tracking.
    """
    # General
    Invalid = -1
    Max = 84

    # Hand
    Hand_Start = 0
    Hand_WristRoot = 0
    Hand_ForearmStub = 1
    Hand_Thumb0 = 2
    Hand_Thumb1 = 3
    Hand_Thumb2 = 4
    Hand_Thumb3 = 5
    Hand_Index1 = 6
    Hand_Index2 = 7
    Hand_Index3 = 8
    Hand_Middle1 = 9
    Hand_Middle2 = 10
    Hand_Middle3 = 11
    Hand_Ring1 = 12
    Hand_Ring2 = 13
    Hand_Ring3 = 14
    Hand_Pinky0 = 15
    Hand_Pinky1 = 16
    Hand_Pinky2 = 17
    Hand_Pinky3 = 18
    Hand_MaxSkinnable = 19
    Hand_ThumbTip = 19
    Hand_IndexTip = 20
    Hand_MiddleTip = 21
    Hand_RingTip = 22
    Hand_PinkyTip = 23
    Hand_End = 24

    # XRHand
    XRHand_Start = 0
    XRHand_Palm = 0
    XRHand_Wrist = 1
    XRHand_ThumbMetacarpal = 2
    XRHand_ThumbProximal = 3
    XRHand_ThumbDistal = 4
    XRHand_ThumbTip = 5
    XRHand_IndexMetacarpal = 6
    XRHand_IndexProximal = 7
    XRHand_IndexIntermediate = 8
    XRHand_IndexDistal = 9
    XRHand_IndexTip = 10
    XRHand_MiddleMetacarpal = 11
    XRHand_MiddleProximal = 12
    XRHand_MiddleIntermediate = 13
    XRHand_MiddleDistal = 14
    XRHand_MiddleTip = 15
    XRHand_RingMetacarpal = 16
    XRHand_RingProximal = 17
    XRHand_RingIntermediate = 18
    XRHand_RingDistal = 19
    XRHand_RingTip = 20
    XRHand_LittleMetacarpal = 21
    XRHand_LittleProximal = 22
    XRHand_LittleIntermediate = 23
    XRHand_LittleDistal = 24
    XRHand_LittleTip = 25
    XRHand_Max = 26
    XRHand_End = 26

    # Body
    Body_Start = 0
    Body_Root = 0
    Body_Hips = 1
    Body_SpineLower = 2
    Body_SpineMiddle = 3
    Body_SpineUpper = 4
    Body_Chest = 5
    Body_Neck = 6
    Body_Head = 7
    Body_LeftShoulder = 8
    Body_LeftScapula = 9
    Body_LeftArmUpper = 10
    Body_LeftArmLower = 11
    Body_LeftHandWristTwist = 12
    Body_RightShoulder = 13
    Body_RightScapula = 14
    Body_RightArmUpper = 15
    Body_RightArmLower = 16
    Body_RightHandWristTwist = 17
    Body_LeftHandPalm = 18
    Body_LeftHandWrist = 19
    Body_LeftHandThumbMetacarpal = 20
    Body_LeftHandThumbProximal = 21
    Body_LeftHandThumbDistal = 22
    Body_LeftHandThumbTip = 23
    Body_LeftHandIndexMetacarpal = 24
    Body_LeftHandIndexProximal = 25
    Body_LeftHandIndexIntermediate = 26
    Body_LeftHandIndexDistal = 27
    Body_LeftHandIndexTip = 28
    Body_LeftHandMiddleMetacarpal = 29
    Body_LeftHandMiddleProximal = 30
    Body_LeftHandMiddleIntermediate = 31
    Body_LeftHandMiddleDistal = 32
    Body_LeftHandMiddleTip = 33
    Body_LeftHandRingMetacarpal = 34
    Body_LeftHandRingProximal = 35
    Body_LeftHandRingIntermediate = 36
    Body_LeftHandRingDistal = 37
    Body_LeftHandRingTip = 38
    Body_LeftHandLittleMetacarpal = 39
    Body_LeftHandLittleProximal = 40
    Body_LeftHandLittleIntermediate = 41
    Body_LeftHandLittleDistal = 42
    Body_LeftHandLittleTip = 43
    Body_RightHandPalm = 44
    Body_RightHandWrist = 45
    Body_RightHandThumbMetacarpal = 46
    Body_RightHandThumbProximal = 47
    Body_RightHandThumbDistal = 48
    Body_RightHandThumbTip = 49
    Body_RightHandIndexMetacarpal = 50
    Body_RightHandIndexProximal = 51
    Body_RightHandIndexIntermediate = 52
    Body_RightHandIndexDistal = 53
    Body_RightHandIndexTip = 54
    Body_RightHandMiddleMetacarpal = 55
    Body_RightHandMiddleProximal = 56
    Body_RightHandMiddleIntermediate = 57
    Body_RightHandMiddleDistal = 58
    Body_RightHandMiddleTip = 59
    Body_RightHandRingMetacarpal = 60
    Body_RightHandRingProximal = 61
    Body_RightHandRingIntermediate = 62
    Body_RightHandRingDistal = 63
    Body_RightHandRingTip = 64
    Body_RightHandLittleMetacarpal = 65
    Body_RightHandLittleProximal = 66
    Body_RightHandLittleIntermediate = 67
    Body_RightHandLittleDistal = 68
    Body_RightHandLittleTip = 69
    Body_End = 70

    # FullBody
    FullBody_Start = 0
    FullBody_Root = 0
    FullBody_Hips = 1
    FullBody_SpineLower = 2
    FullBody_SpineMiddle = 3
    FullBody_SpineUpper = 4
    FullBody_Chest = 5
    FullBody_Neck = 6
    FullBody_Head = 7
    FullBody_LeftShoulder = 8
    FullBody_LeftScapula = 9
    FullBody_LeftArmUpper = 10
    FullBody_LeftArmLower = 11
    FullBody_LeftHandWristTwist = 12
    FullBody_RightShoulder = 13
    FullBody_RightScapula = 14
    FullBody_RightArmUpper = 15
    FullBody_RightArmLower = 16
    FullBody_RightHandWristTwist = 17
    FullBody_LeftHandPalm = 18
    FullBody_LeftHandWrist = 19
    FullBody_LeftHandThumbMetacarpal = 20
    FullBody_LeftHandThumbProximal = 21
    FullBody_LeftHandThumbDistal = 22
    FullBody_LeftHandThumbTip = 23
    FullBody_LeftHandIndexMetacarpal = 24
    FullBody_LeftHandIndexProximal = 25
    FullBody_LeftHandIndexIntermediate = 26
    FullBody_LeftHandIndexDistal = 27
    FullBody_LeftHandIndexTip = 28
    FullBody_LeftHandMiddleMetacarpal = 29
    FullBody_LeftHandMiddleProximal = 30
    FullBody_LeftHandMiddleIntermediate = 31
    FullBody_LeftHandMiddleDistal = 32
    FullBody_LeftHandMiddleTip = 33
    FullBody_LeftHandRingMetacarpal = 34
    FullBody_LeftHandRingProximal = 35
    FullBody_LeftHandRingIntermediate = 36
    FullBody_LeftHandRingDistal = 37
    FullBody_LeftHandRingTip = 38
    FullBody_LeftHandLittleMetacarpal = 39
    FullBody_LeftHandLittleProximal = 40
    FullBody_LeftHandLittleIntermediate = 41
    FullBody_LeftHandLittleDistal = 42
    FullBody_LeftHandLittleTip = 43
    FullBody_RightHandPalm = 44
    FullBody_RightHandWrist = 45
    FullBody_RightHandThumbMetacarpal = 46
    FullBody_RightHandThumbProximal = 47
    FullBody_RightHandThumbDistal = 48
    FullBody_RightHandThumbTip = 49
    FullBody_RightHandIndexMetacarpal = 50
    FullBody_RightHandIndexProximal = 51
    FullBody_RightHandIndexIntermediate = 52
    FullBody_RightHandIndexDistal = 53
    FullBody_RightHandIndexTip = 54
    FullBody_RightHandMiddleMetacarpal = 55
    FullBody_RightHandMiddleProximal = 56
    FullBody_RightHandMiddleIntermediate = 57
    FullBody_RightHandMiddleDistal = 58
    FullBody_RightHandMiddleTip = 59
    FullBody_RightHandRingMetacarpal = 60
    FullBody_RightHandRingProximal = 61
    FullBody_RightHandRingIntermediate = 62
    FullBody_RightHandRingDistal = 63
    FullBody_RightHandRingTip = 64
    FullBody_RightHandLittleMetacarpal = 65
    FullBody_RightHandLittleProximal = 66
    FullBody_RightHandLittleIntermediate = 67
    FullBody_RightHandLittleDistal = 68
    FullBody_RightHandLittleTip = 69
    FullBody_LeftUpperLeg = 70
    FullBody_LeftLowerLeg = 71
    FullBody_LeftFootAnkleTwist = 72
    FullBody_LeftFootAnkle = 73
    FullBody_LeftFootSubtalar = 74
    FullBody_LeftFootTransverse = 75
    FullBody_LeftFootBall = 76
    FullBody_RightUpperLeg = 77
    FullBody_RightLowerLeg = 78
    FullBody_RightFootAnkleTwist = 79
    FullBody_RightFootAnkle = 80
    FullBody_RightFootSubtalar = 81
    FullBody_RightFootTransverse = 82
    FullBody_RightFootBall = 83
    FullBody_End = 84

class SkeletonType(enum.Enum):
    """
    A Python enumeration that corresponds to the C# OVRSkeleton.SkeletonType enum.
    """
    None_ = -1  # Using None_ to avoid conflict with Python's None keyword
    HandLeft = 0
    HandRight = 1
    Body = 2
    FullBody = 3
    XRHandLeft = 4
    XRHandRight = 5

# --- Mappings for get_bone_label ---
# These dictionaries replicate the logic from the C# switch statements.

_HAND_BONE_LABELS: Dict[BoneId, str] = {
    BoneId.Hand_WristRoot: "Hand_WristRoot",
    BoneId.Hand_ForearmStub: "Hand_ForearmStub",
    BoneId.Hand_Thumb0: "Hand_Thumb0",
    BoneId.Hand_Thumb1: "Hand_Thumb1",
    BoneId.Hand_Thumb2: "Hand_Thumb2",
    BoneId.Hand_Thumb3: "Hand_Thumb3",
    BoneId.Hand_Index1: "Hand_Index1",
    BoneId.Hand_Index2: "Hand_Index2",
    BoneId.Hand_Index3: "Hand_Index3",
    BoneId.Hand_Middle1: "Hand_Middle1",
    BoneId.Hand_Middle2: "Hand_Middle2",
    BoneId.Hand_Middle3: "Hand_Middle3",
    BoneId.Hand_Ring1: "Hand_Ring1",
    BoneId.Hand_Ring2: "Hand_Ring2",
    BoneId.Hand_Ring3: "Hand_Ring3",
    BoneId.Hand_Pinky0: "Hand_Pinky0",
    BoneId.Hand_Pinky1: "Hand_Pinky1",
    BoneId.Hand_Pinky2: "Hand_Pinky2",
    BoneId.Hand_Pinky3: "Hand_Pinky3",
    BoneId.Hand_MaxSkinnable: "Hand_ThumbTip",
    BoneId.Hand_IndexTip: "Hand_IndexTip",
    BoneId.Hand_MiddleTip: "Hand_MiddleTip",
    BoneId.Hand_RingTip: "Hand_RingTip",
    BoneId.Hand_PinkyTip: "Hand_PinkyTip",
}

_XRHAND_BONE_LABELS: Dict[BoneId, str] = {
    BoneId.XRHand_Palm: "XRHand_Palm",
    BoneId.XRHand_Wrist: "XRHand_Wrist",
    BoneId.XRHand_ThumbMetacarpal: "XRHand_ThumbMetacarpal",
    BoneId.XRHand_ThumbProximal: "XRHand_ThumbProximal",
    BoneId.XRHand_ThumbDistal: "XRHand_ThumbDistal",
    BoneId.XRHand_ThumbTip: "XRHand_ThumbTip",
    BoneId.XRHand_IndexMetacarpal: "XRHand_IndexMetacarpal",
    BoneId.XRHand_IndexProximal: "XRHand_IndexProximal",
    BoneId.XRHand_IndexIntermediate: "XRHand_IndexIntermediate",
    BoneId.XRHand_IndexDistal: "XRHand_IndexDistal",
    BoneId.XRHand_IndexTip: "XRHand_IndexTip",
    BoneId.XRHand_MiddleMetacarpal: "XRHand_MiddleMetacarpal",
    BoneId.XRHand_MiddleProximal: "XRHand_MiddleProximal",
    BoneId.XRHand_MiddleIntermediate: "XRHand_MiddleIntermediate",
    BoneId.XRHand_MiddleDistal: "XRHand_MiddleDistal",
    BoneId.XRHand_MiddleTip: "XRHand_MiddleTip",
    BoneId.XRHand_RingMetacarpal: "XRHand_RingMetacarpal",
    BoneId.XRHand_RingProximal: "XRHand_RingProximal",
    BoneId.XRHand_RingIntermediate: "XRHand_RingIntermediate",
    BoneId.XRHand_RingDistal: "XRHand_RingDistal",
    BoneId.XRHand_RingTip: "XRHand_RingTip",
    BoneId.XRHand_LittleMetacarpal: "XRHand_LittleMetacarpal",
    BoneId.XRHand_LittleProximal: "XRHand_LittleProximal",
    BoneId.XRHand_LittleIntermediate: "XRHand_LittleIntermediate",
    BoneId.XRHand_LittleDistal: "XRHand_LittleDistal",
    BoneId.XRHand_LittleTip: "XRHand_LittleTip",
}

_BODY_BONE_LABELS: Dict[BoneId, str] = {
    member: f"Body_{member.name.split('_', 1)[1]}" for member in BoneId if member.name.startswith("Body_")
}

_FULLBODY_BONE_LABELS: Dict[BoneId, str] = {
    member: f"FullBody_{member.name.split('_', 1)[1]}" for member in BoneId if member.name.startswith("FullBody_")
}


def get_bone_label(skeleton_type: SkeletonType, bone_id: BoneId) -> Optional[str]:
    """
    Translates a BoneId to a human-readable string label based on the SkeletonType.
    This is a Python port of the C# OVRSkeleton.BoneLabelFromBoneId method.

    Args:
        skeleton_type: The type of skeleton the bone belongs to.
        bone_id: The ID of the bone to label.

    Returns:
        A string label for the bone, or a default/unknown string if not found.
    """
    if skeleton_type in (SkeletonType.HandLeft, SkeletonType.HandRight):
        return _HAND_BONE_LABELS.get(bone_id, "Hand_Unknown")

    if skeleton_type in (SkeletonType.XRHandLeft, SkeletonType.XRHandRight):
        # Note: The original C# code has a complex mapping for XRHand that re-uses
        # Hand_* IDs. For clarity and directness in Python, it's better to use
        # the specific XRHand_* IDs if you have them. If you only have the 0-25 range,
        # you would need a more complex mapping like the C# version.
        # This implementation assumes you can use the correct XRHand_* BoneId members.
        return _XRHAND_BONE_LABELS.get(bone_id, "XRHand_Unknown")

    if skeleton_type == SkeletonType.Body:
        return _BODY_BONE_LABELS.get(bone_id, "Body_Unknown")

    if skeleton_type == SkeletonType.FullBody:
        return _FULLBODY_BONE_LABELS.get(bone_id, "FullBody_Unknown")

    return "Skeleton_Unknown"


# --- Example Usage ---
if __name__ == '__main__':
    print("--- Basic BoneId Info ---")
    wrist_bone = BoneId.Hand_WristRoot
    print(f"Wrist bone: {wrist_bone.name}, Value: {wrist_bone.value}")
    thumb_tip_bone = BoneId(19)
    print(f"Bone with value 19: {thumb_tip_bone.name}")
    print("-" * 20)

    print("\n--- Using get_bone_label ---")
    # Example 1: Get label for a standard hand bone
    bone_id_to_check = BoneId.Hand_IndexTip
    skeleton = SkeletonType.HandRight
    label = get_bone_label(skeleton, bone_id_to_check)
    print(f"The label for {bone_id_to_check.name} in a {skeleton.name} is: '{label}'")

    # Example 2: Get label for a full body bone
    bone_id_to_check = BoneId.FullBody_SpineUpper
    skeleton = SkeletonType.FullBody
    label = get_bone_label(skeleton, bone_id_to_check)
    print(f"The label for {bone_id_to_check.name} in a {skeleton.name} is: '{label}'")

    # Example 3: Get label for an XR hand bone
    bone_id_to_check = BoneId.XRHand_ThumbTip
    skeleton = SkeletonType.XRHandLeft
    label = get_bone_label(skeleton, bone_id_to_check)
    print(f"The label for {bone_id_to_check.name} in a {skeleton.name} is: '{label}'")

    # Example 4: Show an unknown bone
    bone_id_to_check = BoneId.FullBody_RightFootBall
    skeleton = SkeletonType.HandLeft # Incorrect skeleton type for this bone
    label = get_bone_label(skeleton, bone_id_to_check)
    print(f"Trying to find {bone_id_to_check.name} in a {skeleton.name}: '{label}'")

