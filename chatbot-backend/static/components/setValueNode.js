const nodeName = "setValueNode";
const icon = '<i class="fas fa-users-cog"></i>';
const tittleClass = "setValue";
const tittle = "Set Variable to...!";

const component = `
<div>
  <div class="title-box ${tittleClass}">${icon}${tittle}</div>
  <div class="box">
    <p>Variables</p>
    <input type="text" df-saving_keys>
    <p>Type</p>
    <select df-type>
        <option value="text">text</option>
        <option value="number">number</option>
        <option value="boolean">boolean (true/false)</option>
    </select>
    <p>Set to</p>
    <input type="text" df-value>
    </div>
</div>
`;


const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
${icon}<span> ${tittle}</span>
<div id="description_${nodeName}" style="display: none;">
    <p>Set especific session variables to a value</p>
</div>
</div>`
;

export const initSetValueNode = () => {
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

export const addSetValueNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { 
        saving_keys: "[\"last_utterance\"]",
        value: "{name} or especific value",
        type: "text"
    },
    component
  );
};
