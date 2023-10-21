const nodeName = "deciderNode";
const icon = '<i class="fas fa-divide"></i>';
const component = `
<div>
  <div class="title-box decider">${icon}Decider node</div>
  <div class="box">
    <p>Intent list</p>
    <textarea df-intents></textarea>
  </div>
</div>
`;

const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
${icon}<span> Decision Node!</span>
<div id="description_${nodeName}" style="display: none;">
    <p>Makes a decision based on the list (List like ["yes","no","fail"]. If elements provided, it shows the strings as buttons in the UI. If text provided, displays an specific text</p>
</div>
</div>`
;

export const initDeciderNode = () => {
  const menu = document.getElementById("menu-container");
  menu.insertAdjacentHTML("beforeend", menuIcon);
  // Add event listener to show description when dropdown button is clicked
  var descriptionDiv = document.getElementById(`description_${nodeName}`);

    // Get a reference to the element you want to click on
    var element = document.querySelector(`div.drag-drawflow[data-node="${nodeName}"]`);

    // Add a click event listener to the element
    element.addEventListener("click", function () {
        // Toggle the display of the description div
        if (descriptionDiv.style.display === "none") {
            descriptionDiv.style.display = "block";
        } else {
            descriptionDiv.style.display = "none";
        }
    });
};

export const addDeciderNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { 
      intents: "" 
    },
    component
  );
};
