// Add to existing init() function
const originalApplyRoom = window.applyRoom;
window.applyRoom = async function(name) {
    await originalApplyRoom(name);
    if (window.Scene3D) {
        window.Scene3D.changeRoom(name);
    }
};
