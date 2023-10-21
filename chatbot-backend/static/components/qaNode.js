const nodeName = "qaNode";
const icon = '<i class="fas fa-question"></i>';
const tittleClass = "qa";
const tittle = "QA Node";

const component = `
<div>
  <div class="title-box ${tittleClass}">${icon}${tittle}</div>
  <div class="box">
    <p>Collection</p>
    <input type="text" df-collection>
    <p>Question</p>
    <input type="text" df-question>
    <p>Temperature</p>
    <input type="text" df-temperature>
    <p>Max Tokens</p>
    <input type="text" df-max_tokens>
    <p>Model</p>
    <input type="text" df-model>
    <p>Num of Retrieved docs</p>
    <input type="text" df-num_docs>
    <p>Fallback response</p>
    <textarea df-fallback></textarea>

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
    <p>Knowledgebase QA</p>
</div>
</div>`
;

export const initQANode = () => {
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

export const addQANode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { 
        collection: "tenantev",
        question: "{last_utterance}",
        temperature: "0.7",
        max_tokens: "1000",
        model: "gpt-3.5-turbo",
        num_docs: "4",
        fallback: "Sorry, I don't know the answer to that.",
    },
    component
  );
};
