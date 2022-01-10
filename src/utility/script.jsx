var doc = app.activeDocument;
var pages = doc.pages;
var resizeGroup = arguments[0];
var condenseGroup = arguments[1];

// Loop over all available pages separately
for (var pageIndex = 0; pageIndex < pages.length; pageIndex++) {
    var page = pages[pageIndex];
    var pageItems = page.allPageItems;
    var textFrames = [];

    // Collect all TextFrames in an array
    for (var pageItemIndex = 0; pageItemIndex < pageItems.length; pageItemIndex++) {
        var candidate = pageItems[pageItemIndex];
        if (candidate instanceof TextFrame) {
            textFrames.push(candidate);
        }
    }

    // Check if TextFrame overflows, if so add all TextFrames that should be the same size
    for (var textFrameIndex = 0; textFrameIndex < textFrames.length; textFrameIndex++) {
        var textFrame = textFrames[textFrameIndex];

        // If text frame overflows, adjust it and all the frames that are supposed to be of the same size
        if (textFrame.overflows) {
            var foundResizeGroup = filterArrayWithString(resizeGroup, textFrame.name);
            var foundCondenseGroup = filterArrayWithString(condenseGroup, textFrame.name);
            var process = false;
            var chosenGroup, type;

            if (foundResizeGroup.length > 0) {
                chosenGroup = foundResizeGroup;
                type = "resize";
                process = true;
            } else if (foundCondenseGroup.length > 0) {
                chosenGroup = foundCondenseGroup;
                type = "condense";
                process = true;
            }

            if (process) {
                var foundFrames = findTextFramesFromNames(textFrames, chosenGroup);
                adjustTextFrameGroup(foundFrames, type);
            }
        }
    }
}

function adjustTextFrameGroup(resizeGroup, type) {
    // Check if some overflowing textboxes
    if (!someOverflowing(resizeGroup)) {
        return;
    }

    app.scriptPreferences.enableRedraw = false;

    while (someOverflowing(resizeGroup)) {
        for (var textFrameIndex = 0; textFrameIndex < resizeGroup.length; textFrameIndex++) {
            var textFrame = resizeGroup[textFrameIndex];
            if (type === "resize") decreaseFontSize(textFrame);
            else if (type === "condense") condenseFont(textFrame);
            else alert("Unknown operation");
        }
    }

    app.scriptPreferences.enableRedraw = true;
}

function someOverflowing(textFrames) {
    for (var textFrameIndex = 0; textFrameIndex < textFrames.length; textFrameIndex++) {
        var textFrame = textFrames[textFrameIndex];
        if (textFrame.overflows) {
            return true;
        }
    }

    return false;
}

function decreaseFontSize(frame) {
    var texts = frame.parentStory.texts.everyItem().getElements();
    for (var textIndex = 0; textIndex < texts.length; textIndex++) {
        var characters = texts[textIndex].characters.everyItem().getElements();
        for (var characterIndex = 0; characterIndex < characters.length; characterIndex++) {
            characters[characterIndex].pointSize = characters[characterIndex].pointSize - 0.25;
        }
    }
}

function condenseFont(frame) {
    var texts = frame.parentStory.texts.everyItem().getElements();
    for (var textIndex = 0; textIndex < texts.length; textIndex++) {
        var characters = texts[textIndex].characters.everyItem().getElements();
        for (var characterIndex = 0; characterIndex < characters.length; characterIndex++) {
            characters[characterIndex].setNthDesignAxis(1, characters[characterIndex].designAxes[1] - 5)
        }
    }
}

function findTextFramesFromNames(availableFrames, names) {
    var foundFrames = [];

    for (var textFrameIndex = 0; textFrameIndex < availableFrames.length; textFrameIndex++) {
        var textFrame = availableFrames[textFrameIndex];
        if (doesArrayContainString(names, textFrame.name)) {
            foundFrames.push(textFrame);
        }
    }

    return foundFrames;
}

// Pretty lame, would like to use filter() - not available
function filterArrayWithString(arrayToFilter, stringToContain) {
    for (var arrayIndex = 0; arrayIndex < arrayToFilter.length; arrayIndex++) {
        var entry = arrayToFilter[arrayIndex];
        if (doesArrayContainString(entry, stringToContain)) {
            return entry;
        }
    }

    return [];
}

function doesArrayContainString(arrayToCheck, stringToCheck) {
    var doesContain = false;

    for (var arrayIndex = 0; arrayIndex < arrayToCheck.length; arrayIndex++) {
        var entry = arrayToCheck[arrayIndex];
        if (entry === stringToCheck) {
            doesContain = true;
            break;
        }
    }

    return doesContain;
}