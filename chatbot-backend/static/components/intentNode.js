const nodeName = "intentNode";
const icon = '<i class="fas fa-lightbulb"></i>';
const component = `
<div>
  <div class="title-box intent">${icon}Intent node</div>
  <div class="box">
    <p>Intent ("yes/no"...))</p>
    <input type="text" df-intent>
  </div>
</div>
`;

const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
${icon}<span> Intent Node!</span>
<div id="description_${nodeName}" style="display: none;">
    <p>Follows the decision made before, needs to be the same name</p>
</div>
</div>`
;

export const initIntentNode = () => {
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

export const addIntentNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { intent: ""},
    component
  );
};
