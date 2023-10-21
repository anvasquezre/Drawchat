const nodeName = "validatorNode";
const icon = '<i class="fas fa-spell-check"></i>';
const tittleClass = "validator";
const tittle = "User input Validation";

const component = `
<div>
  <div class="title-box ${tittleClass}">${icon}${tittle}</div>
  <div class="box">
    <p>Type</p>
    <select df-type>               
    <option value=\"email\">Email</option>
    <option value=\"id\">Application ID</option>
    </select>
    <p>Variable</p>
    <input type="text" df-variable>

  </div>
</div>
`;


const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
${icon}<span> ${tittle}!</span>
<div id="description_${nodeName}" style="display: none;">
    <p>User input Validation</p>
</div>
</div>`
;

export const initValidatorNode = () => {
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

export const addValidatorNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { 
        type: "email",
        variable: "last_utterance",
    },
    component
  );
};
