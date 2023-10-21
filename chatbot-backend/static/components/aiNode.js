const nodeName = "aiNode";
const icon = '<i class="fas fa-laptop"></i>';
const tittleClass = "ai";
const tittle = "Ask AI";

const component = `
<div>
  <div class="title-box ${tittleClass}">${icon}${tittle}</div>
  <div class="box">
    <p>Instructions</p>
    <textarea df-instruction></textarea>
    <p>System Message</p>
    <textarea df-system_message></textarea>
    <p>Save answer as</p>
    <textarea df-saving_keys></textarea>
    <p>Show answer</p>
    <select df-show>               
    <option value=\"yes\">Yes</option>
    <option value=\"no\">No</option>
    </select>
    <p>Temperature</p>
    <input type="text" df-temperature>
    <p>Max Tokens</p>
    <input type="text" df-max_tokens>
    <p>Model</p>
    <input type="text" df-model>
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
    <p>Ask something to LLM and saves the answer [optional]</p>
</div>
</div>`
;

export const initAINode = () => {
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

export const addAINode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { 
      instruction: "Type Instructions here",
      system_message: "You are a useful assistant",
      saving_keys: '["last_response"]',
      show: "yes",
      temperature: "0.7",
      max_tokens: "1000",
      model: "gpt-3.5-turbo",
    },
    component
  );
};
